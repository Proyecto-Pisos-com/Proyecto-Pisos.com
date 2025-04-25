import folium
from folium.plugins import MarkerCluster
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
from utils import cargar_datos

def show_mapa_coropletico_barrios():
    # --- Cargar datos ---
    @st.cache_data
    def cargar_filtrados():
        return cargar_datos("ventas.csv")

    df = cargar_filtrados()

    # Asegurarse de que 'ubicacion' esté bien tratada
    df['ubicacion'] = df['ubicacion'].str.strip()

    # Calcular la media de precio por ubicación
    media_precio = df.groupby('ubicacion')['precio'].mean().reset_index()
    media_precio.columns = ['Ubicacion', 'Precio Promedio']

    # Unir coordenadas
    media_precio = media_precio.merge(
        df[['ubicacion', 'lat', 'lon', 'habitaciones', 'baños', 'superficie_construida', 'piso', 'casa', 'atico']], 
        left_on='Ubicacion', right_on='ubicacion', how='left'
    )

    # Filtrar ubicaciones sin coordenadas
    media_precio = media_precio.dropna(subset=['lat', 'lon'])

    # --- Funciones auxiliares ---
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

    def obtener_tipo_vivienda(row):
        if row['piso']:
            return 'Piso'
        elif row['casa']:
            return 'Casa'
        elif row['atico']:
            return 'Ático'
        else:
            return 'Otro'

    # --- Crear el mapa base ---
    mapa_precio = folium.Map(location=[40.4168, -3.7038], zoom_start=12)
    marker_cluster_precio = MarkerCluster().add_to(mapa_precio)

    # Agregar marcadores
    for _, row in media_precio.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=f"""
            <strong>{row['Ubicacion']}</strong><br>
            Precio Promedio: {row['Precio Promedio']:.2f} €<br>
            Habitaciones: {row['habitaciones']}<br>
            Baños: {row['baños']}<br>
            Superficie Construida: {row['superficie_construida']} m²<br>
            Tipo de Vivienda: {obtener_tipo_vivienda(row)}
            """,
            icon=folium.Icon(color=obtener_color_precio(row['Precio Promedio']), icon='info-sign')
        ).add_to(marker_cluster_precio)

    # --- Mostrar mapa ---
    st.title("🗺️ Mapa Coroplético - Precio Promedio por Ubicación")
    folium_static(mapa_precio)

    # --- Descripción ---
    st.markdown("""
    Este mapa interactivo muestra la **distribución geográfica de los precios promedio** de los inmuebles en Madrid.

    ### **Interpretación del mapa**:
    - 🔴 Rojo: zonas con **precios altos**
    - 🟠 Naranja: zonas de precios intermedios
    - 🟢 Verde: zonas con **precios bajos**

    Al hacer clic en un marcador, se puede ver:
    - Precio promedio
    - Habitaciones, baños, superficie construida
    - Tipo de vivienda (piso, casa, ático...)

    Este mapa ayuda a visualizar **tendencias geográficas** del mercado inmobiliario.
    """)
