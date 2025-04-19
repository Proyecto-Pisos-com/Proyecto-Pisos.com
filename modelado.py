import pandas as pd
import uuid
from datetime import datetime
import sqlite3

def preparar_df(df, columnas_orden):
        df["timestamp"] = datetime.now().isoformat()
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["id"] = [str(uuid.uuid4()) for _ in range(len(df))]
        df = df[columnas_orden + [col for col in df.columns if col not in columnas_orden]]
        df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
        return df
print("Cargando datos de venta...")
df_venta = pd.read_csv("/Users/carlagamezdelalamo/Documents/GitHub/Proyecto-Pisos.com/venta_madrid_limpio.csv")

df_venta = df_venta.rename(columns={
    "Precio": "precio",
    "Ubicacion": "ubicacion",
    "Habitaciones": "habitaciones",
    "Metros": "metros"
})
df_venta["precio"] = df_venta["precio"].astype(float)
df_venta["habitaciones"] = df_venta["habitaciones"].astype(float)
df_venta["metros"] = df_venta["metros"].astype(float)
df_venta["ubicacion"] = df_venta["ubicacion"].astype(str)

columnas_venta = ["id", "timestamp", "precio", "ubicacion", "habitaciones", "metros"]
df_venta = preparar_df(df_venta, columnas_venta)
df_venta.to_csv("venta_madrid_modelado.csv", index=False)
with sqlite3.connect("venta_madrid.db") as conn:
    df_venta.to_sql("venta_madrid", conn, if_exists="replace", index=False)
print("Venta modelado con éxito.")

print("Cargando datos de alquiler...")
df_alquiler = pd.read_csv("/Users/carlagamezdelalamo/Documents/GitHub/Proyecto-Pisos.com/alquiler_madrid_limpio.csv")

df_alquiler["Superficie_construida"] = df_alquiler["Superficie_construida"].astype(float)
df_alquiler["Tipo_vivienda"] = df_alquiler["Tipo_vivienda"].astype(str)

columnas_alquiler = ["id", "timestamp", "Tipo_vivienda", "Superficie_construida"]
df_alquiler = preparar_df(df_alquiler, columnas_alquiler)

df_alquiler.to_csv("alquiler_madrid_modelado.csv", index=False)
with sqlite3.connect("alquiler_madrid.db") as conn:
    df_alquiler.to_sql("alquiler_madrid", conn, if_exists="replace", index=False)
print("Alquiler modelado con éxito.")

print("\nVista previa de los datos de venta:")
print(df_venta.head())
print("\nVista previa de los datos de alquiler:")
print(df_alquiler.head())
print("\nDatos de venta guardados en 'venta_madrid_modelado.csv' y 'venta_madrid.db'")
print("Datos de alquiler guardados en 'alquiler_madrid_modelado.csv' y 'alquiler_madrid.db'")
# Guardar en SQLite
with sqlite3.connect("venta_madrid.db") as conn:
    df_venta.to_sql("venta_madrid", conn, if_exists="replace", index=False)
    df_alquiler.to_sql("alquiler_madrid", conn, if_exists="replace", index=False)
print("Datos guardados en SQLite.")
# Guardar en CSV
df_venta.to_csv("venta_madrid_modelado.csv", index=False)
df_alquiler.to_csv("alquiler_madrid_modelado.csv", index=False)
print("Datos guardados en CSV.")

