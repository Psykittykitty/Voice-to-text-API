import os


TMP_DIR = os.environ.get("WHISPER_TMP_DIR", "/tmp")
# Whisper 模型名，默认用 small
WHISPER_MODEL = os.environ.get("WHISPER_MODEL", "small")
