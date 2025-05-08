import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
from streamlit.components.v1 import html
from utils import cargar_datos
from config import ALQUILER_CSV

def show_graficos_extra():
    @st.cache_data
    def cargar_filtrados():
        df = cargar_datos(ALQUILER_CSV)
        return df.dropna(subset=["precio", "lat", "lon", "ubicacion"])

    df = cargar_filtrados()

    st.title("📊 Gráficos Adicionales de Análisis Inmobiliario")

    # --- Mapa interactivo con fondo claro ---
    st.subheader("Ubicación geográfica y precios")
    m = folium.Map(location=[df["lat"].mean(), df["lon"].mean()], zoom_start=13, tiles=None)
    folium.TileLayer("CartoDB positron").add_to(m)
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in df.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=f"<b>{row['titulo']}</b><br>Precio: {row['precio']} €<br>Ubicación: {row['ubicacion']}",
            tooltip=row["titulo"]
        ).add_to(marker_cluster)

    folium_static_path = "mapa_alquiler_folium.html"
    m.save(folium_static_path)
    with open(folium_static_path, 'r', encoding='utf-8') as f:
        html(f.read(), height=500)

    # --- Boxplot ordenado (izq. más caro → der. más barato) ---
    st.subheader("Distribución de Precios por Zona")

    # Ordenar zonas por precio medio
    orden_zonas = df.groupby("ubicacion")["precio"].mean().sort_values(ascending=False).index.tolist()
    df["ubicacion"] = pd.Categorical(df["ubicacion"], categories=orden_zonas, ordered=True)

    # Crear gráfico boxplot ordenado
    fig_box = px.box(
        df.sort_values("ubicacion"),  # Asegura orden visual en el gráfico
        x="ubicacion",
        y="precio",
        points="outliers",
        hover_data=["titulo", "precio", "habitaciones", "baños", "superficie_construida"],
        labels={"ubicacion": "Zona", "precio": "Precio (€)"},
        title="Variabilidad de precios por zona"
    )

    fig_box.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_box, use_container_width=True)

    # --- Descripción final ---
    st.markdown("""
    Estos gráficos permiten al usuario:
    - 📍 Ver sobre el mapa cómo varía el precio por ubicación.
    - 📦 Detectar zonas con precios atípicos o muy variables.
    - ℹ️ Comparar inmuebles con info útil como superficie, habitaciones y estado.
    """)
