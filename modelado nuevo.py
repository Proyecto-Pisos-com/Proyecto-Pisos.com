import pandas as pd
import sqlite3
from datetime import datetime
df = pd.read_csv('venta_madrid_limpio.csv')
# Conectar a la base de datos SQLite
conexion = sqlite3.connect('venta_madrid.db')
# Crear un cursor para ejecutar consultas SQL
cursor = conexion.cursor()
# Crear una tabla para almacenar los datos de ventas
cursor.execute('''
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY,
    fecha_venta TEXT,
    precio_venta REAL,
    tipo TEXT,
    ubicacion TEXT,
    habitaciones INTEGER,
    banos INTEGER,
    superficie REAL,
    antiguedad INTEGER,
    calefaccion TEXT,
    aire_acondicionado TEXT,
    piscina TEXT,
    garaje TEXT
)''')
# Insertar los datos del DataFrame en la tabla
df.to_sql('ventas', conexion, if_exists='replace', index=False)
# Cerrar la conexión
conexion.close()
# Crear un DataFrame de ejemplo
# df = pd.DataFrame({
#     'id': [1, 2, 3],
#     'fecha_venta': ['2023-01-01', '2023-02-01', '2023-03-01'],
#     'precio_venta': [200000, 250000, 300000],
#     'tipo': ['piso', 'casa', 'apartamento'],
#     'ubicacion': ['Madrid', 'Barcelona', 'Valencia'],
#     'habitaciones': [2, 3, 4],
#     'banos': [1, 2, 2],
#     'superficie': [80, 120, 150],
#     'antiguedad': [5, 10, 15],
#     'calefaccion': ['central', 'individual', 'eléctrica'],
#     'aire_acondicionado': ['central', 'individual', 'no tiene'],
#     'piscina': ['privada', 'comunitaria', 'no tiene'],
#     'garaje': ['privado', 'comunitario', 'no tiene']
# })
# Guardar el DataFrame en un archivo CSV
# df.to_csv('venta_madrid.csv', index=False, encoding='utf-8')
# # Cargar el archivo CSV
# df = pd.read_csv('venta_madrid.csv', encoding='utf-8')
# # Eliminar columnas innecesarias
# columnas_a_eliminar = ['id', 'nombre', 'descripcion', 'url']
# df.drop(columns=columnas_a_eliminar, inplace=True)
# # Renombrar columnas
# df.rename(columns={'fecha': 'fecha_venta', 'precio': 'precio_venta'}, inplace=True)
# # Convertir la columna 'fecha_venta' a tipo datetime
# df['fecha_venta'] = pd.to_datetime(df['fecha_venta'], format='%Y-%m-%d')
# # Eliminar filas con valores nulos
# df.dropna(inplace=True)
# # Eliminar duplicados
# df.drop_duplicates(inplace=True)
# # Filtrar por precio
# precio_minimo = 10000
# precio_maximo = 500000
# df = df[(df['precio_venta'] >= precio_minimo) & (df['precio_venta'] <= precio_maximo)]
# # Filtrar por fecha
# fecha_inicio = '2022-01-01'
# fecha_fin = '2023-12-31'
# df = df[(df['fecha_venta'] >= fecha_inicio) & (df['fecha_venta'] <= fecha_fin)]
# # Filtrar por tipo de propiedad
# tipos_permitidos = ['piso', 'casa', 'apartamento']
# df = df[df['tipo'].isin(tipos_permitidos)]
# # Filtrar por ubicación
# ubicaciones_permitidas = ['Madrid', 'Barcelona', 'Valencia']
# df = df[df['ubicacion'].isin(ubicaciones_permitidas)]
# # Filtrar por número de habitaciones
# numero_habitaciones_minimo = 1
# numero_habitaciones_maximo = 5
# df = df[(df['habitaciones'] >= numero_habitaciones_minimo) & (df['habitaciones'] <= numero_habitaciones_maximo)]
# # Filtrar por superficie
# superficie_minima = 30
# superficie_maxima = 300
# df = df[(df['superficie'] >= superficie_minima) & (df['superficie'] <= superficie_maxima)]
# # Filtrar por antigüedad
# antiguedad_maxima = 20
# df = df[df['antiguedad'] <= antiguedad_maxima]
# # Filtrar por precio por metro cuadrado
# precio_metro_cuadrado_minimo = 1000
# precio_metro_cuadrado_maximo = 5000
# df['precio_metro_cuadrado'] = df['precio_venta'] / df['superficie']
# df = df[(df['precio_metro_cuadrado'] >= precio_metro_cuadrado_minimo) & (df['precio_metro_cuadrado'] <= precio_metro_cuadrado_maximo)]
# # Filtrar por número de baños
# numero_banos_minimo = 1
# numero_banos_maximo = 3
# df = df[(df['banos'] >= numero_banos_minimo) & (df['banos'] <= numero_banos_maximo)]
# # Filtrar por tipo de calefacción
# tipos_calefaccion_permitidos = ['central', 'individual', 'eléctrica']
# df = df[df['calefaccion'].isin(tipos_calefaccion_permitidos)]
# # Filtrar por tipo de aire acondicionado
# tipos_aire_acondicionado_permitidos = ['central', 'individual', 'no tiene']
# df = df[df['aire_acondicionado'].isin(tipos_aire_acondicionado_permitidos)]
# # Filtrar por tipo de piscina
# tipos_piscina_permitidos = ['privada', 'comunitaria', 'no tiene']
# df = df[df['piscina'].isin(tipos_piscina_permitidos)]
# # Filtrar por tipo de garaje
# tipos_garaje_permitidos = ['privado', 'comunitario', 'no tiene']
# df = df[df['garaje'].isin(tipos_garaje_permitidos)]
# # Filtrar por tipo de terraza
# tipos_terraza_permitidos = ['privada', 'comunitaria', 'no tiene']
# df = df[df['terraza'].isin(tipos_terraza_permitidos)]
# # Eliminar la columna 'precio_metro_cuadrado'
# df.drop(columns=columnas_a_eliminar, inplace=True)
# # Guardar el DataFrame limpio en un nuevo archivo CSV
df.to_csv('venta_madrid_limpio.csv', index=False, encoding='utf-8')
# # Cargar el archivo CSV limpio
df = pd.read_csv('venta_madrid_limpio.csv', encoding='utf-8')
df.to_sql('ventas', conexion, if_exists='replace', index=False)
# Cerrar la conexión
conexion.close()
print("Datos guardados en la base de datos SQLite.")
