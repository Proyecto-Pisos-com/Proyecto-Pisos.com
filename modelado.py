import pandas as pd
import uuid
from datetime import datetime
import sqlite3
df = pd.read_csv("venta_madrid_limpio.csv")
df["timestamp"] = datetime.now() .isoformat()
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["id"] = [str(uuid.uuid4()) for _ in range(len(df))]
primeras_columnas = ["id", "timestamp", "Precio", "Ubicacion", "Habitaciones", "Metros"]
otras_columnas = [col for col in df.columns if col not in primeras_columnas]
df = df[primeras_columnas + otras_columnas]
df = df.rename(columns={
    "Precio": "precio",
    "Ubicacion": "ubicacion",
    "Habitaciones": "habitaciones",
    "Metros": "metros"
})
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["id"] = df["id"].astype(str)
df["precio"] = df["precio"].astype(float)
df["ubicacion"] = df["ubicacion"].astype(str)
df["habitaciones"] = df["habitaciones"].astype(float)
df["metros"] = df["metros"].astype(float)
df["id"] = df["id"].astype(str)
df.to_csv("venta_madrid_modelado.csv", index=False)
print("El archivo 'venta_madrid_modelado.csv' ha sido creado con éxito.")
# El archivo 'venta_madrid_modelado.csv' ha sido creado con éxito.
print('\nvista previa del archivo:')
print(df.head(10))ls data/venta_madrid.db
print('\nestadísticas del archivo:')
print(df[["precio", "habitaciones", "metros"]].describe())
# Conexión a la base de datos SQLite
conn = sqlite3.connect("venta_madrid.db")
# Guardar el DataFrame en la base de datos
df.to_sql("venta_madrid", conn, if_exists="replace", index=False)
# Cerrar la conexión
conn.close()
print("El DataFrame ha sido guardado en la base de datos 'venta_madrid.db' en la tabla 'venta_madrid'.")
# El DataFrame ha sido guardado en la base de datos 'venta_madrid.db' en la tabla 'venta_madrid'.