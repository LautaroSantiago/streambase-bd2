"""
db.py — Módulo de conexión a MongoDB
StreamBase | Grupo 14 | BD2 | Div133 | UTN Avellaneda
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Carga las variables definidas en el archivo .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME   = os.getenv("DB_NAME", "streambase")


def get_db():
    """
    Devuelve una tupla (client, db).
    El llamador es responsable de cerrar el cliente con client.close()
    una vez que termina de operar — buena práctica vista en clase.
    """
    client = MongoClient(MONGO_URI)
    db     = client[DB_NAME]
    return client, db
