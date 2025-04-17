import pandas as pd
import numpy as np
import re
import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Tuple
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
with open('venta_madrid_completo.json', 'r', encoding='utf-8') as archivo:
    data = json.load(archivo)
# Convertir la lista de diccionarios a un DataFrame
df = pd.DataFrame(data)
# Configuración del registro
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Definir el nombre del archivo CSV
nombre_archivo_csv = 'venta_madrid_completo.csv'
# Guardar el DataFrame en un archivo CSV
df.to_csv(nombre_archivo_csv, index=False, encoding='utf-8')
# Cargar el archivo CSV
df = pd.read_csv(nombre_archivo_csv, encoding='utf-8')
# Eliminar columnas innecesarias
columnas_a_eliminar = ['id', 'nombre', 'descripcion', 'url']
df.drop(columns=columnas_a_eliminar, inplace=True)
# Renombrar columnas
df.rename(columns={'fecha': 'fecha_venta', 'precio': 'precio_venta'}, inplace=True)
# Convertir la columna 'fecha_venta' a tipo datetime
df['fecha_venta'] = pd.to_datetime(df['fecha_venta'], format='%Y-%m-%d')
# Eliminar filas con valores nulos
df.dropna(inplace=True)
# Eliminar duplicados
df.drop_duplicates(inplace=True)
# Filtrar por precio
precio_minimo = 10000
precio_maximo = 500000
df = df[(df['precio_venta'] >= precio_minimo) & (df['precio_venta'] <= precio_maximo)]
# Filtrar por fecha
fecha_inicio = '2022-01-01'
fecha_fin = '2023-12-31'
df = df[(df['fecha_venta'] >= fecha_inicio) & (df['fecha_venta'] <= fecha_fin)]
# Filtrar por tipo de propiedad
tipos_permitidos = ['piso', 'casa', 'apartamento']
df = df[df['tipo'].isin(tipos_permitidos)]
# Filtrar por ubicación
ubicaciones_permitidas = ['Madrid', 'Barcelona', 'Valencia']
df = df[df['ubicacion'].isin(ubicaciones_permitidas)]
# Filtrar por número de habitaciones
numero_habitaciones_minimo = 1
numero_habitaciones_maximo = 5
df = df[(df['habitaciones'] >= numero_habitaciones_minimo) & (df['habitaciones'] <= numero_habitaciones_maximo)]
# Filtrar por superficie
superficie_minima = 30
superficie_maxima = 300
df = df[(df['superficie'] >= superficie_minima) & (df['superficie'] <= superficie_maxima)]
# Filtrar por antigüedad
antiguedad_maxima = 20
df = df[df['antiguedad'] <= antiguedad_maxima]
# Filtrar por precio por metro cuadrado
precio_metro_cuadrado_minimo = 1000
precio_metro_cuadrado_maximo = 5000
df['precio_metro_cuadrado'] = df['precio_venta'] / df['superficie']
df = df[(df['precio_metro_cuadrado'] >= precio_metro_cuadrado_minimo) & (df['precio_metro_cuadrado'] <= precio_metro_cuadrado_maximo)]
# Filtrar por número de baños
numero_banos_minimo = 1
numero_banos_maximo = 3
df = df[(df['banos'] >= numero_banos_minimo) & (df['banos'] <= numero_banos_maximo)]
# Filtrar por tipo de calefacción
tipos_calefaccion_permitidos = ['central', 'individual', 'eléctrica']
df = df[df['calefaccion'].isin(tipos_calefaccion_permitidos)]
# Filtrar por tipo de aire acondicionado
tipos_aire_acondicionado_permitidos = ['central', 'individual', 'no tiene']
df = df[df['aire_acondicionado'].isin(tipos_aire_acondicionado_permitidos)]
# Filtrar por tipo de piscina
tipos_piscina_permitidos = ['privada', 'comunitaria', 'no tiene']
df = df[df['piscina'].isin(tipos_piscina_permitidos)]
# Filtrar por tipo de garaje
tipos_garaje_permitidos = ['privado', 'comunitario', 'no tiene']
df = df[df['garaje'].isin(tipos_garaje_permitidos)]
# Filtrar por tipo de terraza
tipos_terraza_permitidos = ['privada', 'comunitaria', 'no tiene']
df = df[df['terraza'].isin(tipos_terraza_permitidos)]
columnas_a_eliminar = ['precio_metro_cuadrado']
df.drop(columns=columnas_a_eliminar, inplace=True)
for columna in df.select_dtypes(include=['object']).columns:
    df[columna] = df[columna].str.strip().str.lower()
# Guardar el DataFrame limpio en un nuevo archivo CSV
nombre_archivo_csv_limpio = 'venta_madrid_limpio.csv'
df.to_csv(nombre_archivo_csv_limpio, index=False, encoding='utf-8')
# Guardar el DataFrame limpio en un archivo JSON
nombre_archivo_json_limpio = 'venta_madrid_limpio.json'
df.to_json(nombre_archivo_json_limpio, orient='records', lines=True, force_ascii=False)
print(f"El DataFrame limpio se ha guardado en {nombre_archivo_json_limpio}")




