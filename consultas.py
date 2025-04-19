import sqlite3
import pandas as pd

# ----------- VENTAS -----------
print("[VENTA] Conectando con la base de datos...")
conn_venta = sqlite3.connect("venta_madrid.db")

print("\n[VENTA] Pisos con más de 3 habitaciones:")
df_venta_hab = pd.read_sql_query(
    "SELECT * FROM venta_madrid WHERE habitaciones > 3", conn_venta)
print(df_venta_hab)

print("\n[VENTA] Pisos con más de 90 metros:")
df_venta_metros = pd.read_sql_query(
    "SELECT * FROM venta_madrid WHERE metros > 90", conn_venta)
print(df_venta_metros)

print("\n[VENTA] Pisos con más de 200000 euros:")
df_venta_precio = pd.read_sql_query(
    "SELECT * FROM venta_madrid WHERE precio > 200000", conn_venta)
print(df_venta_precio)

conn_venta.close()


# ----------- ALQUILER -----------
print("\n[ALQUILER] Consultando base de datos...")
conn_alquiler = sqlite3.connect("alquiler_madrid.db")

print("\n[ALQUILER] Inmuebles con más de 90m² construidos:")
df_alq_superficie = pd.read_sql_query(
    "SELECT * FROM alquiler_madrid WHERE Superficie_construida > 90", conn_alquiler)
print(df_alq_superficie)

conn_alquiler.close()
