import whisper
from pathlib import Path

# Funcion para que whisper transcriba audio con extract_audio
def extract_audio(file_path: str, language: str = "es") -> str:
    try:
        extracted_text = extract_audio_whisper(file_path, language)
        cleaned_text = replacement(extracted_text)
        return cleaned_text
    except Exception as e:
        print(f"Error extrayendo audio: {e}")
        return ""

# Funcion para todo el proceso de extraccion 
def extract_audio_whisper(path: str, language: str = "es") -> str:    
    try:
        path = Path(path)
        print("Cargando modelo Whisper 'base'...")
        model = whisper.load_model("base")
        print("Modelo cargado. Iniciando transcripción...")
        result = model.transcribe(str(path), language=language, verbose=True)
        print("Transcripción terminada.")
        return result["text"].strip()
    except Exception as e:
        print(f"Error transcribiendo audio: {e}")
        return ""

# Funcion para quitar parentesis y signos
def replacement(text: str) -> str:
    return text.replace("(", "").replace(")", "").replace("\u2014", "")
