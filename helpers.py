import re


def normalize_ellipsis(text):
    return re.sub(r"\.{2,}", "...", text)


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
