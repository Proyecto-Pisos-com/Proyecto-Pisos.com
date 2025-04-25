import os
import pandas as pd
from dotenv import load_dotenv

def load_credentials():
    load_dotenv()
    return {
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "database": os.getenv("DB_NAME"),
    }

def cargar_datos(nombre_archivo):
    """Carga un CSV desde ../data relativo a app.py"""
    ruta = os.path.join(os.path.dirname(__file__), "..", "data", nombre_archivo)
    if os.path.exists(ruta):
        return pd.read_csv(ruta)
    return pd.DataFrame()

