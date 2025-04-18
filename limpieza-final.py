import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
df1 = pd.read_json("/Users/carlagamezdelalamo/Documents/GitHub/Proyecto-Pisos.com/venta_madrid_detalle_completo.json")
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
df1["Precio"] = df1["Precio"].astype(str)
df1["Precio"] = df1["Precio"].replace({r"[€.,\s]": ""}, regex=True)
df1["Precio"] = df1["Precio"].replace("", np.nan)
df1["Precio"] = pd.to_numeric(df1["Precio"], errors="coerce")
df1["Habitaciones"] = df1["Habitaciones"].astype(str)
df1["Habitaciones"] = df1["Habitaciones"].replace({r"[^\d]": ""}, regex=True)
df1["Habitaciones"] = df1["Habitaciones"].replace("", np.nan)
df1["Habitaciones"] = pd.to_numeric(df1["Habitaciones"], errors="coerce")
df1["Metros"] = df1["Metros"].astype(str)
df1["Metros"] = df1["Metros"].replace({r"[^\d]": ""}, regex=True)
df1["Metros"] = df1["Metros"].replace("", np.nan)
df1["Metros"] = pd.to_numeric(df1["Metros"], errors="coerce")
df1["Ubicacion"] = df1["Ubicacion"].astype(str)
if "descripcion_ampliada" in df1.columns:
    df1["descripcion_ampliada"] = df1["descripcion_ampliada"].astype(str)
    df1["descripcion_ampliada"] = df1["descripcion_ampliada"].str.lower()
    df1["descripcion_ampliada"] = df1["descripcion_ampliada"].str.strip()
    df1["descripcion_ampliada"] = df1["descripcion_ampliada"].replace(r"\s+", " ", regex=True)
print("\nTipos de datos después de la limpieza:")
print("Con 'Madrid' en Ubicacion:", len(df1[df1["Ubicacion"].str.contains("Madrid")]))
print("Habitaciones >= 3:", len(df1[df1["Habitaciones"] >= 3]))
print("Metros >= 90:", len(df1[df1["Metros"] >= 90]))
print("Precio >= 200000:", len(df1[df1["Precio"] >= 200000]))
print("\nEstadísticas tras limpieza:")
print(df1[["Precio", "Habitaciones", "Metros"]].describe())
df1 = df1[df1["Ubicacion"].str.contains("Madrid", na=False)]
df1 = df1[df1["Habitaciones"] >= 3]
df1 = df1[df1["Metros"] >= 90]
df1 = df1[df1["Precio"] >= 200000]
df1.to_csv("venta_madrid_limpio.csv", index=False)
df1 = pd.read_csv("venta_madrid_limpio.csv")
print(df1.head())
