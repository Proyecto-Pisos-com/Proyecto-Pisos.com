import streamlit as st
from utils import cargar_datos
  # usamos la función que creamos

def show_data_page():
    st.title("📊 Visualización de Alquileres en Madrid")

    # Cargar el archivo 'alquiler.csv' desde la carpeta /data
    df = cargar_datos("alquiler.csv")

    if df.empty:
        st.error("⚠️ No se pudo cargar el archivo alquiler.csv")
        return

    st.write("### Primeras filas del dataset")
    st.dataframe(df.head())

    if "precio" in df.columns:
        st.write("### Estadísticas de precios")
        st.write(df["precio"].describe())
    else:
        st.warning("La columna 'precio' no se encuentra en el dataset.")
