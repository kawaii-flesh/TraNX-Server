import re


def normalize_ellipsis(text):
    return re.sub(r"\.{2,}", "...", text)


def get_aspect_ratio(text):
    cjk_count = sum(1 for ch in text if is_cjk(ch))
    return 1.05 if cjk_count / max(len(text), 1) > 0.5 else 0.57


def is_cjk(char):
    return any(
        [
            "\u4e00" <= char <= "\u9fff",  # CJK Unified Ideographs
            "\u3040" <= char <= "\u309f",  # Hiragana
            "\u30a0" <= char <= "\u30ff",  # Katakana
            "\uac00" <= char <= "\ud7af",  # Hangul
        ]
    )


def is_cjk_text(text):
    cjk_count = sum(1 for char in text if is_cjk(char))
    return cjk_count / max(len(text), 1) > 0.5


def wrap_text(text, max_chars_per_line):
    if is_cjk_text(text):
        lines, current_line = [], ""
        for char in text:
            current_line += char
            if len(current_line) >= max_chars_per_line:
                lines.append(current_line)
                current_line = ""
        if current_line:
            lines.append(current_line)
        return "\n".join(lines)
    else:
        lines, current_line, length = [], [], 0
        for word in text.split():
            word_length = len(word)
            if length + word_length + (1 if current_line else 0) <= max_chars_per_line:
                current_line.append(word)
                length += word_length + (1 if current_line else 0)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                length = word_length
        if current_line:
            lines.append(" ".join(current_line))
        return "\n".join(lines)


def to_hex_16(num):
    return f"{num:016X}"


def split_into_sentences(text):
    text = normalize_ellipsis(text)
    sentences = []
    current_sentence = ""
    i = 0
    n = len(text)
    while i < n:
        char = text[i]
        current_sentence += char

        if char in {".", "!", "?", "。", "！", "？"}:
            if char == "." and i + 2 < n and text[i + 1] == "." and text[i + 2] == ".":
                current_sentence += ".."
                i += 2
            sentences.append(current_sentence.strip())
            current_sentence = ""
        i += 1
    if current_sentence.strip():
        sentences.append(current_sentence.strip())
    return sentences
