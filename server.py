from flask import Flask, request, jsonify, render_template, send_from_directory
import base64
from io import BytesIO
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
import os
import json
from paddleocr import PaddleOCR
import time
import re
from symspellpy import SymSpell, Verbosity
import argparse
import helpers
from tnx_translator import Translator, get_translator

# https://en.wikipedia.org/wiki/ISO_639-3
LANGUAGE_CODES = ["eng", "rus", "ukr", "deu", "fra", "jpn", "kor", "zho", "zht"]
# https://github.com/PaddlePaddle/PaddleOCR/blob/fd5b4e1049b758cf29b3c922a19b4c5f4ec47b88/docs/version2.x/ppocr/blog/multi_languages.en.md
OCR_LANG_MAP = {
    "eng": "en",
    "rus": "ru",
    "ukr": "uk",
    "deu": "german",
    "fra": "fr",
    "jpn": "japan",
    "kor": "korean",
    "zho": "ch",
    "zht": "chinese_cht",
}

SAVE_DIR = "./data"
DEFAULT_CONFIG = {
    "version": "4.0.0",
    "image_processing": {
        "contrast": 1.0,
        "brightness": 1.0,
        "sharpness": 1.0,
        "threshold": -1,
        "blur_radius": 0,
        "invert": False,
    },
    "paddleocr": {"use_angle_cls": True, "rec_algorithm": "CRNN"},
    "translation": {"src_lang": LANGUAGE_CODES[0], "dest_lang": LANGUAGE_CODES[1]},
    "text_processing": {"enable_symspellpy": False, "split_sentences": True},
    "frames": {
        "translation_frame": {"startX": 0, "startY": 0, "endX": 0, "endY": 0},
        "output_frame": {"startX": 0, "startY": 0, "endX": 0, "endY": 0},
    },
}

app = Flask(__name__)
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

global_pid = None
sym_spell = None
translator: Translator = None


def load_dynamic_parts(config):
    global sym_spell
    if config["text_processing"]["enable_symspellpy"]:
        if sym_spell is None:
            print(">>> Loading SymSpell...")
            sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
            dictionary_path = "./dictionaries/frequency_dictionary_en_82_765.txt"
            sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
    else:
        sym_spell = None


def get_pid_dir(pid):
    pid_dir = os.path.join(SAVE_DIR, pid)
    if not os.path.exists(pid_dir):
        os.makedirs(pid_dir)
    return pid_dir


def get_config_path():
    return os.path.join(get_pid_dir(global_pid), "config.json")


def load_config():
    config_path = get_config_path()
    config_needs_saving = False  # Flag to indicate if config was created/reset

    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
            current_major_version = config.get("version", "1.0.0").split(".")[0]
            default_major_version = DEFAULT_CONFIG["version"].split(".")[0]
            if current_major_version != default_major_version:
                new_path = f"{config_path}.v{config.get('version', '1.0.0')}"
                os.rename(config_path, new_path)
                config_needs_saving = True
    else:
        config_needs_saving = True

    if config_needs_saving:
        config = DEFAULT_CONFIG.copy()
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)

    load_dynamic_parts(config)
    return config


def save_config(config):
    config_path = get_config_path()
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)
    load_dynamic_parts(config)


def spell_correct(text):
    global sym_spell
    if sym_spell is None:
        return text
    try:
        words = re.findall(r"\w+(?:-\w+)*|[^\w\s]", text)
        corrected = []
        corrections = []

        for word in words:
            if word.isalpha():
                is_capitalized = word[0].isupper()
                original_word = word

                if word.lower() in sym_spell.words:
                    corrected.append(word)
                    continue

                suggestions = sym_spell.lookup(
                    word.lower(), Verbosity.CLOSEST, max_edit_distance=1
                )
                if suggestions:
                    suggestions.sort(key=lambda s: abs(len(s.term) - len(word.lower())))
                    best = suggestions[0].term

                    if is_capitalized:
                        best = best.capitalize()

                    if best.lower() != word.lower():
                        corrections.append(f"{word} -> {best}")

                    corrected.append(best)
                else:
                    corrected.append(word)
            else:
                corrected.append(word)

        if corrections:
            print("Corrections made:")
            for correction in corrections:
                print(correction)

        return re.sub(r"\s+([.,!?;:])", r"\1", " ".join(corrected))
    except Exception as e:
        print(f"[ERROR] SymSpell correction failed: {e}")
        return text


def apply_image_processing(image, settings):
    if settings["contrast"] != 1.0:
        image = ImageEnhance.Contrast(image).enhance(settings["contrast"])
    if settings["brightness"] != 1.0:
        image = ImageEnhance.Brightness(image).enhance(settings["brightness"])
    if settings["sharpness"] != 1.0:
        image = ImageEnhance.Sharpness(image).enhance(settings["sharpness"])
    if settings["blur_radius"] > 0:
        image = image.filter(ImageFilter.GaussianBlur(settings["blur_radius"]))
    if settings["threshold"] > 0:
        image = image.convert("L").point(
            lambda p: 255 if p > settings["threshold"] else 0
        )
    if settings["invert"]:
        image = Image.eval(image, lambda x: 255 - x)
    return image


def run_ocr(image: Image.Image, config):
    ocr = PaddleOCR(
        use_angle_cls=config["paddleocr"]["use_angle_cls"],
        lang=OCR_LANG_MAP.get(config["translation"]["src_lang"], "en"),
        rec_algorithm=config["paddleocr"]["rec_algorithm"],
        det_db_score_mode="slow",
    )
    results = ocr.ocr(np.asarray(image), cls=True)
    if not results:
        return None, "No text recognized"
    text = " ".join([line[1][0] for line in results[0]])
    if config["text_processing"]["enable_symspellpy"]:
        text = spell_correct(text)
    return text, None


@app.route("/")
def index_pid():
    global global_pid
    origin_exists = os.path.exists(os.path.join(SAVE_DIR, f"{global_pid}_origin.png"))
    timestamp = str(time.time())
    config = load_config()
    return render_template(
        "index.html",
        config=config,
        origin_exists=origin_exists,
        timestamp=timestamp,
        pid=global_pid,
    )


@app.route("/save_config/<pid>", methods=["POST"])
def save_config_pid(pid):
    global global_pid
    global_pid = pid
    try:
        new_config_data = request.json
        config = load_config()

        # Apply updates from new_config_data
        if "image_processing" in new_config_data:
            config["image_processing"].update(new_config_data["image_processing"])
        if "text_processing" in new_config_data:
            config["text_processing"].update(new_config_data["text_processing"])

        # Handle translation update
        if "translation" in new_config_data:
            config["translation"].update(new_config_data["translation"])

        save_config(
            config
        )  # save_config just dumps to json and calls load_dynamic_parts
        process_current_image()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


def process_current_image():
    origin_path = os.path.join(get_pid_dir(global_pid), "original.png")
    if not os.path.exists(origin_path):
        return False
    config = load_config()
    image = Image.open(origin_path)
    processed_image = apply_image_processing(image, config["image_processing"])
    processed_image.save(os.path.join(get_pid_dir(global_pid), "processed.png"))
    return True


@app.route("/process_image/<pid>", methods=["POST"])
def process_image_pid(pid):
    global global_pid
    global_pid = pid
    if not process_current_image():
        return jsonify({"error": "No origin image found"}), 400
    return jsonify(
        {
            "original": f"/image/{pid}/original?"
            + str(os.path.getmtime(os.path.join(SAVE_DIR, f"{pid}_origin.png"))),
            "processed": f"/image/{pid}/processed?"
            + str(os.path.getmtime(os.path.join(SAVE_DIR, f"{pid}_processed.png"))),
        }
    )


def process_ocr_and_translation(image: Image.Image, config):
    extracted_text, error = run_ocr(image, config)
    if error:
        return None, None, error

    sentences = [extracted_text]
    if config["text_processing"]["split_sentences"]:
        sentences = helpers.split_into_sentences(extracted_text)
    src_lang = translator.convert_lang_code(
        config["translation"]["src_lang"], LANGUAGE_CODES
    )
    dest_lang = translator.convert_lang_code(
        config["translation"]["dest_lang"], LANGUAGE_CODES
    )
    translated_text = " ".join(translator.translate(sentences, src_lang, dest_lang))

    return extracted_text, translated_text, None


@app.route("/recognize_text/<pid>", methods=["POST"])
def recognize_text_pid(pid):
    global global_pid
    global_pid = pid
    processed_path = os.path.join(SAVE_DIR, f"{pid}_processed.png")
    if not os.path.exists(processed_path):
        return jsonify({"error": "No processed image found"}), 400

    config = load_config()
    image = Image.open(processed_path)
    extracted_text, translated_text, error = process_ocr_and_translation(image, config)
    if error:
        return jsonify({"error": error}), 400

    return jsonify(
        {"recognized_text": extracted_text, "translated_text": translated_text}
    )


@app.route("/image/<pid>/<type>")
def get_image_pid(pid, type):
    filename = (
        "original.png"
        if type == "original"
        else "processed.png" if type == "processed" else None
    )
    if not filename:
        return "Not found", 404
    return send_from_directory(get_pid_dir(pid), filename)


def check_frame(frame):
    return (
        frame.get("startX", 0) != 0
        or frame.get("startY", 0) != 0
        or frame.get("endX", 0) != 0
        or frame.get("endY", 0) != 0
    )


@app.route("/upload", methods=["POST"])
def upload_screenshot():
    global global_pid
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    if "pid" not in request.form:
        return jsonify({"error": "No PID provided"}), 400

    image_file = request.files["image"]
    global_pid = helpers.to_hex_16(int(request.form["pid"]))
    print(f"PID: {global_pid}")
    pid_dir = get_pid_dir(global_pid)

    try:
        image = Image.open(image_file.stream)
        config = load_config()

        translation_frame_req = json.loads(request.form.get("translationFrame", "{}"))
        output_frame_req = json.loads(request.form.get("outputFrame", "{}"))

        request_has_translation_frame = check_frame(translation_frame_req)

        request_has_output_frame = check_frame(output_frame_req)

        config_changed = False
        if request_has_translation_frame:
            config["frames"]["translation_frame"] = translation_frame_req
            config_changed = True
        if request_has_output_frame:
            config["frames"]["output_frame"] = output_frame_req
            config_changed = True

        translation_frame = config["frames"]["translation_frame"]
        output_frame = config["frames"]["output_frame"]
        if config_changed:
            save_config(config)

        if not (check_frame(translation_frame)):
            return jsonify(
                {
                    "text": "At least the translation frame must be specified!",
                    "x": 10,
                    "y": 0,
                    "width": 0,
                    "height": 24,
                    "translation_frame": {
                        "startX": 0,
                        "startY": 0,
                        "endX": 0,
                        "endY": 0,
                    },
                    "output_frame": {"startX": 0, "startY": 0, "endX": 0, "endY": 0},
                    "use_output_frame": False,
                }
            )

        def get_coords(frame):
            return (
                min(frame["startX"], frame["endX"]),
                min(frame["startY"], frame["endY"]),
                max(frame["startX"], frame["endX"]),
                max(frame["startY"], frame["endY"]),
            )

        use_output_frame = check_frame(output_frame)
        start_x, start_y, end_x, end_y = get_coords(translation_frame)
        render_x, render_y, render_end_x, render_end_y = get_coords(
            output_frame if use_output_frame else translation_frame
        )

        if (
            start_x >= end_x
            or start_y >= end_y
            or render_x >= render_end_x
            or render_y >= render_end_y
        ):
            return jsonify({"error": "Invalid translation or output area"}), 400

        cropped_image = image.crop((start_x, start_y, end_x, end_y))
        cropped_image.save(os.path.join(pid_dir, "original.png"))

        processed_image = apply_image_processing(
            cropped_image, config["image_processing"]
        )
        processed_image.save(os.path.join(pid_dir, "processed.png"))

        _, translated_text, error = process_ocr_and_translation(processed_image, config)
        if error:
            return jsonify({"error": error}), 400

        frame_width = render_end_x - render_x
        frame_height = render_end_y - render_y
        font_height = frame_height
        aspect_ratio = helpers.get_aspect_ratio(translated_text)

        while True:
            char_width = font_height * aspect_ratio
            max_chars_per_line = int(frame_width / char_width)
            wrapped_text = helpers.wrap_text(translated_text, max_chars_per_line)
            lines_count = len(wrapped_text.split("\n"))
            total_height = lines_count * font_height
            if total_height <= frame_height and font_height > 1:
                break
            font_height -= 1

        response = {
            "text": wrapped_text,
            "x": render_x,
            "y": render_y,
            "width": frame_width,
            "height": font_height,
            "translation_frame": translation_frame,
            "output_frame": output_frame,
            "use_output_frame": use_output_frame,
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run OCR translation server.")
    parser.add_argument(
        "--translator",
        type=str,
        choices=["nllb", "google", "baidu", "aliyun", "tencent", "youdao"],
    )
    args = parser.parse_args()

    translator = get_translator(args.translator)
    app.run(host="0.0.0.0", port=1785)
