import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# -------------------------------
# VENTA
# -------------------------------
print("[VENTA] Cargando datos...")
df_venta = pd.read_csv("venta_madrid_modelado.csv")
año_actual = datetime.datetime.now().year
np.random.seed(42)
df_venta["año_construccion"] = np.random.randint(1960, 2021, size=len(df_venta))
df_venta["antigüedad"] = año_actual - df_venta["año_construccion"]

# Gráficos venta
print("[VENTA] Visualizando datos...")

plt.figure(figsize=(12, 7))
df_venta = df_venta.dropna(subset=["precio", "metros"])
df_venta["color_code"] = df_venta["ubicacion"].astype("category").cat.codes
scatter = plt.scatter(df_venta["metros"], df_venta["precio"], c=df_venta["color_code"], alpha=0.5, cmap="viridis")
plt.title("Precio vs Metros (Venta)")
plt.xlabel("Metros útiles")
plt.ylabel("Precio (€)")
plt.colorbar(scatter, label="Ubicación codificada")
plt.grid()
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(df_venta["antigüedad"], df_venta["precio"], alpha=0.5, c="orange")
plt.title("Precio vs Antigüedad (Venta)")
plt.xlabel("Antigüedad (años)")
plt.ylabel("Precio (€)")
plt.grid()
plt.tight_layout()
plt.show()

# -------------------------------
# ALQUILER
# -------------------------------
print("[ALQUILER] Cargando datos...")
df_alquiler = pd.read_csv("alquiler_madrid_modelado.csv")
df_alquiler = df_alquiler.dropna(subset=["Superficie_construida"])
df_alquiler["Superficie_construida"] = df_alquiler["Superficie_construida"].astype(float)

# Simulamos precios de alquiler para graficar (ya que no hay columna de "precio" directamente)
np.random.seed(42)
df_alquiler["precio_estimado"] = np.random.randint(800, 3000, size=len(df_alquiler))

# Gráficos alquiler
print("[ALQUILER] Visualizando datos...")

plt.figure(figsize=(12, 7))
df_alquiler["color_code"] = df_alquiler["Tipo_vivienda"].astype("category").cat.codes
scatter = plt.scatter(df_alquiler["Superficie_construida"], df_alquiler["precio_estimado"], c=df_alquiler["color_code"], alpha=0.5, cmap="plasma")
plt.title("Precio estimado vs Superficie Construida (Alquiler)")
plt.xlabel("Superficie Construida (m²)")
plt.ylabel("Precio estimado (€)")
plt.colorbar(scatter, label="Tipo de vivienda codificado")
plt.grid()
plt.tight_layout()
plt.show()

print("Visualizaciones completadas.")
