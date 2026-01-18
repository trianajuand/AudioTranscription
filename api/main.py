from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import RedirectResponse
import tempfile
import os

from etl.database import DatabaseHandler

app = FastAPI()


def get_db():
    return DatabaseHandler()


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        db = get_db()
        result = db.add_audio(tmp_path)

        os.remove(tmp_path)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
