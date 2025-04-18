import sqlite3
import pandas as pd
conn = sqlite3.connect("venta_madrid.db")
print('\npisos con más de 3 habitaciones:')
df = pd.read_sql_query("SELECT * FROM venta_madrid WHERE habitaciones > 3", conn)
print(df)
print('\npisos con más de 90 metros:')
df = pd.read_sql_query("SELECT * FROM venta_madrid WHERE metros > 90", conn)
print(df)
print('\npisos con más de 200000 euros:')
df = pd.read_sql_query("SELECT * FROM venta_madrid WHERE precio > 200000", conn)
print(df)
conn.close()
# Cerrar la conexión
# print("La conexión a la base de datos ha sido cerrada.")
# # La conexión a la base de datos ha sido cerrada.
# print("El archivo 'venta_madrid_modelado.csv' ha sido creado con éxito.")
