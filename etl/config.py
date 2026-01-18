import os
import shutil
from pathlib import Path

def setup_ffmpeg():
    # 1️⃣ Si ffmpeg ya está disponible (Render / Linux)
    if shutil.which("ffmpeg"):
        return

    # 2️⃣ Ruta local Windows (raw string)
    local_ffmpeg = Path(
        r"C:\Users\juand\Downloads\ffmpeg-2026-01-14-git-6c878f8b82-full_build\bin\ffmpeg.exe"
    )

    if local_ffmpeg.exists():
        os.environ["PATH"] = str(local_ffmpeg.parent) + os.pathsep + os.environ.get("PATH", "")
        return

    # 3️⃣ Error claro
    raise RuntimeError("FFmpeg no encontrado")
