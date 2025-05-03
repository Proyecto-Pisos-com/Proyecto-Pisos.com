import streamlit as st
from cargar_datos import cargar_datos
from filtros import aplicar_filtros
from entrenar_modelo import entrenar_modelo
from graficas import mostrar_grafico
import pickle

# 1️⃣ Título de la aplicación
st.title("🏡 Predicción del Precio de Viviendas con Redes Neuronales")

# 2️⃣ Selección de dataset
archivo = st.selectbox("📂 Selecciona el dataset:", ["alquiler.csv", "ventas.csv"])
st.write(f"🔎 Cargando datos desde **{archivo}**...")

# 3️⃣ Cargar datos
df = cargar_datos(archivo)

# 4️⃣ Aplicar filtros interactivos
df = aplicar_filtros(df)

# 5️⃣ Mostrar vista previa del dataset
st.subheader("📊 Vista previa de los datos:")
st.dataframe(df.head())

# 6️⃣ Selección de columnas para el modelo
columnas_usar = ["habitaciones", "baños", "metros", "precio", "precio_m2", "superficie_construida", "superficie_util", "conservacion", "tipo_vivienda"]
columnas_disponibles = [col for col in columnas_usar if col in df.columns]

# 7️⃣ Entrenar el modelo si hay suficientes datos
if "precio" in df.columns and all(col in df.columns for col in columnas_disponibles):
    st.subheader("⚙️ Entrenando la red neuronal para predecir precios...")
    
    modelo, predicciones, y_test, mse = entrenar_modelo(df, columnas_disponibles)
    st.success(f"✅ Modelo entrenado con éxito. Error cuadrático medio (MSE): {mse:,.2f}")

    # 8️⃣ Mostrar gráfica con transformación logarítmica
    mostrar_grafico(y_test, predicciones)

    # 9️⃣ Guardar y descargar el modelo entrenado
    st.subheader("💾 Descargar modelo entrenado")
    modelo_serializado = pickle.dumps(modelo)
    st.download_button("⬇️ Descargar modelo (.pkl)", modelo_serializado, file_name="modelo_entrenado.pkl")

else:
    st.warning("⚠️ Faltan columnas clave para entrenar el modelo.")
