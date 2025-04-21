import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import os

def show_data_page():
    """ Vista de datos de alquiler con filtros y mapa interactivo. """

    st.title("📊 Comparador de Alquileres en Madrid")

    csv_path = r"E:\Proyecto Final Bootcamp - copia\Proyecto Final\Pisos.com\Proyecto speed 1\Data Alquiler Unificado\alquiler_unificado_con_coordenadas_unicos.csv"

    if not os.path.exists(csv_path):
        st.error(f"⚠️ Archivo CSV no encontrado en la ruta: {csv_path}")
        return

    data = pd.read_csv(csv_path)

    st.sidebar.title("🔍 Filtrar datos")

    if "titulo_y" in data.columns:
        titulo = st.sidebar.selectbox("Selecciona un inmueble:", data["titulo_y"].unique())
    else:
        st.warning("⚠️ La columna 'titulo_y' no existe en el archivo CSV.")
        return

    if "precio_num" in data.columns:
        precio_max = st.sidebar.slider("Precio máximo (€)", int(data["precio_num"].min()), int(data["precio_num"].max()), step=100)
    else:
        st.warning("⚠️ La columna 'precio_num' no existe en el archivo CSV.")
        return

    data_filtrada = data[(data["titulo_y"] == titulo) & (data["precio_num"] <= precio_max)]

    st.subheader("📊 Datos filtrados")
    st.dataframe(data_filtrada)

    if {"lat", "lon"}.issubset(data.columns) and not data_filtrada.empty:
        st.subheader("📍 Ubicación en el mapa")

        lat = data_filtrada["lat"].iloc[0]
        lon = data_filtrada["lon"].iloc[0]

        m = folium.Map(location=[lat, lon], zoom_start=15)

        for _, row in data_filtrada.iterrows():
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=row["titulo_y"],
                tooltip=row["ubicacion_y"]
            ).add_to(m)

        folium_static(m)
    else:
        st.warning("⚠️ No se encontraron coordenadas para mostrar en el mapa.")
