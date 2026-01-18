"""
Manejo de MongoDB para el proyecto ETL de audios.
"""

from typing import Any, Dict, List
import os
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from etl.extract import extract_audio


DB_NAME = "sample_mflix"
COLLECTION_NAME = "audios_transcritos"


class DatabaseHandler:
    def __init__(self) -> None:
        mongo_uri = os.getenv("MONGO_URI")

        if not mongo_uri:
            raise RuntimeError("La variable de entorno MONGO_URI no está definida")

        try:
            self.client = MongoClient(
                mongo_uri,
                tls=True,
                tlsAllowInvalidCertificates=True,
                serverSelectionTimeoutMS=5000,
            )

            db = self.client[DB_NAME]
            self.collection = db[COLLECTION_NAME]

            # 🔹 El índice NO debe tumbar la app si falla
            try:
                self.collection.create_index([("texto", "text")])
            except PyMongoError as e:
                print("⚠️ No se pudo crear el índice, continuando:", e)

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
            "created_at": datetime.utcnow(),
        }

        self.collection.insert_one(document)
        return document

    def get_audios(self) -> List[Dict[str, Any]]:
        return list(self.collection.find({}, {"_id": 0}))
