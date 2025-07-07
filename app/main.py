from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse
from app.transcript import transcribe_and_clean  # 绝对导入

app = FastAPI(title="Whisper Transcription API")

@app.post("/transcribe", response_class=PlainTextResponse)
async def transcribe(file: UploadFile = File(...)):
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=415, detail="只支持 audio/* 文件")
    content = await file.read()
    text = transcribe_and_clean(content, file.filename)
    return text

@app.get("/health")
def health_check():
    return {"status": "ok"}
