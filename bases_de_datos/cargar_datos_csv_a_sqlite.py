import pandas as pd
import sqlite3
from config import ALQUILER_CSV, VENTAS_CSV, DATABASE_ALQUILER, DATABASE_VENTAS  

# Columnas esperadas en la tabla
columnas_esperadas = [
    "titulo", "precio", "ubicacion", "habitaciones", "baños", "metros",
    "superficie_construida", "superficie_util", "tipo_vivienda",
    "descripcion_ampliada", "link", "precio_m2"
]

# Columnas booleanas para tipo de vivienda
lista_tipos_vivienda = ["piso", "atico", "estudio", "apartamento", "duplex", "chalet", "finca", "loft"]

# --- Generar tipo_vivienda desde columnas booleanas ---
def generar_tipo_vivienda(df):
    df = df.copy()

    # Verificar que solo haya un True por fila
    boolean_matrix = df[lista_tipos_vivienda].fillna(False).astype(bool)
    suma_booleans = boolean_matrix.sum(axis=1)

    # Filtrar filas con más de un True
    conflictivas = df[suma_booleans > 1]
    if not conflictivas.empty:
        print(f"⚠️ Se encontraron {len(conflictivas)} filas con múltiples tipos de vivienda marcados. Serán eliminadas.")
        df = df[suma_booleans <= 1]

    # Asignar tipo de vivienda
    df["tipo_vivienda"] = boolean_matrix.to_numpy().argmax(axis=1)
    df["tipo_vivienda"] = df["tipo_vivienda"].apply(lambda val: lista_tipos_vivienda[val])

    return df

# --- Preparar DataFrame unificado ---
def preparar_dataframe(ruta_csv):
    df = pd.read_csv(ruta_csv)

    # Si tiene las columnas booleanas → generar tipo_vivienda
    if all(col in df.columns for col in lista_tipos_vivienda):
        df = generar_tipo_vivienda(df)

    # Añadir columnas faltantes
    for col in columnas_esperadas:
        if col not in df.columns:
            df[col] = pd.NA

    return df[columnas_esperadas]

# --- Guardar DataFrame en SQLite ---
def guardar_en_sqlite(df, ruta_sqlite):
    conn = sqlite3.connect(ruta_sqlite)
    df.to_sql("anuncios", conn, if_exists="replace", index=False)
    conn.close()
    print(f"✅ Base de datos guardada en: {ruta_sqlite}")

# --- Crear las dos bases ---
df_alquiler = preparar_dataframe(ALQUILER_CSV)
guardar_en_sqlite(df_alquiler, DATABASE_ALQUILER)

df_ventas = preparar_dataframe(VENTAS_CSV)
guardar_en_sqlite(df_ventas, DATABASE_VENTAS)
