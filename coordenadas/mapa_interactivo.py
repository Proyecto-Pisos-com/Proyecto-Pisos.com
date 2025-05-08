import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from utils import cargar_datos
from config import ALQUILER_CSV 

def show_mapa_interactivo():
    st.title("🗺️ Mapa Precio Promedio por Zona en Alquiler")

    @st.cache_data
    def cargar_filtrados():
        df = cargar_datos(ALQUILER_CSV)  
        return df.dropna(subset=["lat", "lon", "ubicacion", "titulo", "precio", "link"])

    df = cargar_filtrados()

    tipo_cols = [
        ("piso", "Piso"),
        ("casa", "Casa"),
        ("atico", "Ático"),
        ("estudio", "Estudio"),
        ("apartamento", "Apartamento"),
        ("duplex", "Dúplex"),
        ("chalet", "Chalet"),
        ("finca", "Finca"),
        ("loft", "Loft"),
    ]

    def detectar_tipo(row):
        for col, nombre in tipo_cols:
            if col in row and row[col] == 1:
                return nombre
        return "Otro"

    df["tipo_vivienda"] = df.apply(detectar_tipo, axis=1)

    if {"lat", "lon", "precio", "ubicacion"}.issubset(df.columns):
        st.subheader("📍 Mapa Precio Promedio por Ubicación")

        df['ubicacion'] = df['ubicacion'].str.strip()
        media_precio = df.groupby('ubicacion')['precio'].mean().reset_index()
        media_precio.columns = ['Ubicacion', 'Precio Promedio']

        media_precio = media_precio.merge(
            df[['ubicacion', 'lat', 'lon', 'habitaciones', 'baños', 'superficie_construida', 'tipo_vivienda']],
            left_on='Ubicacion', right_on='ubicacion', how='left'
        )
        media_precio = media_precio.dropna(subset=['lat', 'lon'])

        min_precio = media_precio['Precio Promedio'].min()
        max_precio = media_precio['Precio Promedio'].max()

        def obtener_color_precio(precio):
            normalized_price = (precio - min_precio) / (max_precio - min_precio)
            if normalized_price < 0.33:
                return 'green'
            elif normalized_price > 0.66:
                return 'red'
            else:
                return 'orange'

        mapa_precio = folium.Map(location=[40.4168, -3.7038], zoom_start=12, tiles="CartoDB positron")
        marker_cluster_precio = MarkerCluster().add_to(mapa_precio)

        for _, row in media_precio.iterrows():
            tipo = row.get("tipo_vivienda", "Otro")
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=f"""
                    <strong>{row['Ubicacion']}</strong><br>
                    Precio Promedio: {row['Precio Promedio']:.2f} €<br>
                    Habitaciones: {row['habitaciones']}<br>
                    Baños: {row['baños']}<br>
                    Superficie Construida: {row['superficie_construida']} m²<br>
                    Tipo de Vivienda: {tipo}
                """,
                icon=folium.Icon(color=obtener_color_precio(row['Precio Promedio']), icon='info-sign')
            ).add_to(marker_cluster_precio)

        # 👉 Mostrar en columnas
        col_mapa, col_info = st.columns([3, 1])
        with col_mapa:
            st_folium(mapa_precio, width="100%", height=600)

        with col_info:
            st.markdown("### ℹ️ Interpretación del mapa")
            st.markdown("- 🔴 **Rojo**: zonas con precios **altos**")
            st.markdown("- 🟠 **Naranja**: zonas con precios **intermedios**")
            st.markdown("- 🟢 **Verde**: zonas con precios **bajos**")
    else:
        st.warning("⚠️ No se encontraron las columnas necesarias para el mapa interactivo.")
