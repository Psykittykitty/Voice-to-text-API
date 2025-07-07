import os
import re
import uuid
import whisper

pattern_hhmmss = r"\[\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\]"
pattern_mmss   = r"\[\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}\.\d{3}\]"
timestamp_pattern = f"(?:{pattern_hhmmss}|{pattern_mmss})"

model = whisper.load_model("small")

def clean_text(txt_path: str) -> str:
    lines = []
    with open(txt_path, "r", encoding="utf-8") as f:
        for line in f:
            text = re.sub(timestamp_pattern, "", line).strip()
            if text:
                lines.append(text)
    return " ".join(lines)

def transcribe_and_clean(file_content: bytes, filename: str) -> str:
    temp_audio = f"/tmp/{uuid.uuid4().hex}_{filename}"
    with open(temp_audio, "wb") as f:
        f.write(file_content)

    result = model.transcribe(temp_audio, verbose=True)
    temp_txt = temp_audio + ".txt"
    with open(temp_txt, "w", encoding="utf-8") as f_txt:
        for seg in result["segments"]:
            f_txt.write(f"[{seg['start']:.3f} --> {seg['end']:.3f}]  {seg['text'].strip()}\n")

    clean = clean_text(temp_txt)
    os.remove(temp_audio)
    os.remove(temp_txt)
    return clean
