"""Manejo de MongoDB para el proyecto ETL de audios."""

from typing import Any, Dict, List
import os
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from etl.extract import extract_audio

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "sample_mflix"
COLLECTION_NAME = "audios_transcritos"


class DatabaseHandler:
    def __init__(self) -> None:
        if not MONGO_URI:
            raise RuntimeError("MONGO_URI no está definido")

        try:
            self.client = MongoClient(MONGO_URI)
            db = self.client[DB_NAME]
            self.collection = db[COLLECTION_NAME]
            self.collection.create_index([("texto", "text")])
        except PyMongoError as e:
            raise RuntimeError(f"Error al conectar con MongoDB: {e}")

    def add_audio(self, path: str) -> Dict[str, Any]:
        if not path:
            raise ValueError("El path no puede estar vacío.")

        texto = extract_audio(path)

        if not texto:
            raise RuntimeError("El audio no contiene texto válido.")

        document = {
            "filename": os.path.basename(path),
            "texto": texto,
            "created_at": datetime.utcnow()
        }

        try:
            self.collection.insert_one(document)
            return document
        except PyMongoError as e:
            raise RuntimeError(f"Error al insertar en MongoDB: {e}")

    def get_audios(self) -> List[Dict[str, Any]]:
        return list(self.collection.find({}, {"_id": 0}))

    def remove_all(self) -> int:
        result = self.collection.delete_many({})
        return result.deleted_count
