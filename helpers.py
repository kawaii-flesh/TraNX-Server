import re

def normalize_ellipsis(text):
    return re.sub(r"\.{2,}", "...", text)

def wrap_text(text, max_chars_per_line):
    lines, current_line, length = [], [], 0
    for word in text.split():
        if length + len(word) + (1 if current_line else 0) <= max_chars_per_line:
            current_line.append(word)
            length += len(word) + (1 if current_line else 0)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
            length = len(word)
    if current_line:
        lines.append(" ".join(current_line))
    return "\n".join(lines)

def to_hex_16(num):
    return f"{num:016X}"

def split_into_sentences(text):
    text = normalize_ellipsis(text)
    sentences, current = [], ""
    i = 0
    while i < len(text):
        current += text[i]
        if text[i] in ".!?":
            if text[i:i+3] == "...":
                current += ".."
                i += 2
            sentences.append(current.strip())
            current = ""
        i += 1
    if current.strip():
        sentences.append(current.strip())
    return sentences