import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

def show_detail_page():
    """ Vista detallada con información de cada inmueble en venta. """
    
    st.title("🔍 Comparador de Inmuebles en Venta en Madrid")

    try:
        data = pd.read_csv(r"E:\Proyecto Final Bootcamp - copia\Proyecto Final\Pisos.com\Proyecto speed 1\Data Venta Madrid\venta_madrid.csv")  
    except FileNotFoundError:
        st.error("⚠️ Archivo CSV no encontrado. Verifica la ruta.")
        return  

    selected_inmueble = st.selectbox("Selecciona un inmueble:", data["titulo"].unique())

    inmueble_data = data[data["titulo"] == selected_inmueble]

    st.subheader("🏠 Detalles del inmueble")
    st.dataframe(inmueble_data)

    if {"lat", "lon"}.issubset(data.columns) and not inmueble_data.empty:
        st.subheader("📍 Ubicación en el mapa")

        lat = inmueble_data["lat"].iloc[0]
        lon = inmueble_data["lon"].iloc[0]

        m = folium.Map(location=[lat, lon], zoom_start=15)

        folium.Marker(
            location=[lat, lon],
            popup=selected_inmueble,
            tooltip="Ubicación exacta"
        ).add_to(m)

        folium_static(m)
    else:
        st.warning("⚠️ No se encontraron coordenadas para mostrar en el mapa.")
