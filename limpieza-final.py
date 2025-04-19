
import pandas as pd
import numpy as np
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

df1 = pd.read_json("venta_madrid_detalle_completo.json")
df2 = pd.read_json("detalles_alquiler_madrid_completo.json")

print(df1[["precio", "ubicacion", "habitaciones", "metros"]].head(10))
print("\nTipos de datos:")
print(df1[["precio", "ubicacion", "habitaciones", "metros"]].dtypes)
print("\nNulos por columna:")
print(df1[["precio", "ubicacion", "habitaciones", "metros"]].isnull().sum())

df1 = df1.rename(columns={
    "precio": "Precio",
    "ubicacion": "Ubicacion",
    "habitaciones": "Habitaciones",
    "metros": "Metros"
})
df2 = df2.rename(columns={
    "descripcion": "Descripcion",
    "tipo_vivienda": "Tipo_vivienda",
    "superficie_construida": "Superficie_construida",
    "url": "Url"
})

df1 = df1.dropna(subset=["Precio", "Ubicacion", "Habitaciones", "Metros"])

df1["Precio"] = pd.to_numeric(df1["Precio"].astype(str).replace({r"[€.,\s]": ""}, regex=True), errors="coerce")
df1["Habitaciones"] = pd.to_numeric(df1["Habitaciones"].astype(str).replace({r"[^\d]": ""}, regex=True), errors="coerce")
df1["Metros"] = pd.to_numeric(df1["Metros"].astype(str).replace({r"[^\d]": ""}, regex=True), errors="coerce")
df1["Ubicacion"] = df1["Ubicacion"].astype(str)

if "descripcion_ampliada" in df1.columns:
    df1["descripcion_ampliada"] = (
        df1["descripcion_ampliada"]
        .astype(str)
        .str.replace(r"[\n\r]", " ", regex=True)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

print("\nTipos de datos después de la limpieza:")
print("Con 'Madrid' en Ubicacion:", len(df1[df1["Ubicacion"].str.contains("Madrid")]))
print("Habitaciones >= 3:", len(df1[df1["Habitaciones"] >= 3]))
print("Metros >= 90:", len(df1[df1["Metros"] >= 90]))
print("Precio >= 200000:", len(df1[df1["Precio"] >= 200000]))
print("\nEstadísticas tras limpieza:")
print(df1[["Precio", "Ubicacion", "Habitaciones", "Metros"]].describe())

df1 = df1[
    (df1["Ubicacion"].str.contains("Madrid")) &
    (df1["Habitaciones"] >= 3) &
    (df1["Metros"] >= 90) &
    (df1["Precio"] >= 200000)
]

df1.to_csv("venta_madrid_limpio.csv", index=False)

df2 = df2.dropna(subset=["Descripcion", "Tipo_vivienda", "Superficie_construida", "Url"])
df2["Descripcion"] = df2["Descripcion"].astype(str).str.lower().str.replace(r"[\n\r]", " ", regex=True).str.replace(r"\s+", " ", regex=True).str.strip()
df2["Tipo_vivienda"] = df2["Tipo_vivienda"].astype(str).str.lower().str.strip()
df2["Url"] = df2["Url"].astype(str).str.lower()
df2["Superficie_construida"] = pd.to_numeric(df2["Superficie_construida"].astype(str).replace({r"[^\d]": ""}, regex=True), errors="coerce")

print("\n ANÁLISIS DE COLUMNAS EN df2:")
print("Total de registros antes de filtros:", len(df2))
print("\nValores únicos en Tipo_vivienda:")
print(df2["Tipo_vivienda"].dropna().unique())
print("\nEjemplos de Descripcion:")
print(df2["Descripcion"].dropna().head(10).to_list())
print("\nEstadísticas de Superficie_construida:")
print(df2["Superficie_construida"].describe())

print("\nFilas antes del filtrado:", len(df2))
df2 = df2[df2["Descripcion"].str.contains("madrid", na=False)]
print("Después de filtrar por 'madrid':", len(df2))
df2 = df2[df2["Superficie_construida"] >= 90]
print("Después de filtrar por Superficie_construida >= 90:", len(df2))
# df2 = df2[df2["Tipo_vivienda"].str.contains("piso|apartamento|ático|estudio|loft", case=False, na=False)]print("Después de filtrar por Tipo_vivienda:", len(df2))
df2.to_csv("alquiler_madrid_limpio.csv", index=False)

# Guardar los DataFrames limpios en archivos CSV
df1.to_csv("venta_madrid_limpio.csv", index=False)
df2.to_csv("alquiler_madrid_limpio.csv", index=False)

print("\nVENTAS:")
print(df1.head())
print("\nALQUILERES:")
print(df2.head())
print("\nArchivos CSV generados: 'venta_madrid_limpio.csv' y 'alquiler_madrid_limpio.csv'")
