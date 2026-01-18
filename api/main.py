from fastapi import FastAPI, UploadFile, File, HTTPException
from etl.config import setup_ffmpeg
from etl.database import DatabaseHandler
import tempfile
import os

setup_ffmpeg()

app = FastAPI(
    title="ETL Whisper API",
    version="1.0.0"
)

db = DatabaseHandler()

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".wav", ".mp3", ".m4a", ".ogg", ".flac")):
        raise HTTPException(status_code=400, detail="Formato de audio no soportado")

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as temp_audio:
            temp_audio.write(await file.read())
            temp_path = temp_audio.name

        document = db.add_audio(temp_path)

        return {
            "filename": document["filename"],
            "transcription": document["texto"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
