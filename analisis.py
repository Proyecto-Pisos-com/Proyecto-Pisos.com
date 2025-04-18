import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

df = pd.read_csv("venta_madrid_modelado.csv")
# df = pd.read_csv("venta_madrid_limpio.csv")
año_actual = datetime.datetime.now().year
np.random.seed(42)
df["año_construccion"] = np.random.randint(1960, 2021, size=len(df))
df["antigüedad"] = año_actual - df["año_construccion"]
df = df.dropna(subset=["precio"])

df["superficie_construida"] = df["superficie_construida"].astype(str)
df["superficie_construida"] = df["superficie_construida"].replace({r"[^\d]": ""}, regex=True)
df["superficie_construida"] = pd.to_numeric(df["superficie_construida"], errors="coerce")
df = df.dropna(subset=["superficie_construida"])
df["color_code"] = df["ubicacion"].astype("category").cat.codes
plt.figure(figsize=(12, 7))
scatter = plt.scatter(
    df["superficie_construida"],
    df["precio"],
    c=df["color_code"],
    alpha=0.5,
    cmap="viridis"
)
plt.title("Relación entre Superficie Construida y precio")
plt.xlabel("Superficie Construida (m²)")
plt.ylabel("precio (€)")
plt.grid(True)
cbar = plt.colorbar(scatter)
cbar.set_label("Zonas / Barrios codificados")
plt.tight_layout()
plt.show()
print("Gráfico de dispersión entre Superficie Construida y precio con color por ubicación")
# Gráfico de dispersión entre Superficie Construida y precio
# con color por ubicación
plt.figure(figsize=(10, 6))
scatter = plt.scatter(df["superficie_construida"], df["precio"], alpha=0.5)
plt.title("Relación entre Superficie Construida y precio")
plt.xlabel("Superficie Construida (m²)")
plt.ylabel("precio (€)")
plt.grid()
plt.show()
print("Gráfico de dispersión entre Superficie Construida y precio")
df = df.dropna(subset=["precio", "antigüedad"])
plt.figure(figsize=(10, 6))
plt.scatter(df["antigüedad"], df["precio"], alpha=0.6, c="orange")
plt.title("Relación entre Antigüedad y Precio (valores simulados)")
plt.xlabel("Antigüedad (años)")
plt.ylabel("Precio (€)")
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/precio_vs_antiguedad.png")
plt.show()
print("Gráfico de dispersión entre Antigüedad y precio")
# Gráfico de dispersión entre Antigüedad y precio
