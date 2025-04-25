import streamlit as st
import pandas as pd
import plotly.express as px
from utils import cargar_datos

def show_graficos_extra():
    # --- Cargar datos ---
    @st.cache_data
    def cargar_filtrados():
        df = cargar_datos("alquiler.csv")
        return df.dropna(subset=["precio", "lat", "lon", "ubicacion"])

    df = cargar_filtrados()

    st.title("📊 Gráficos Adicionales de Análisis Inmobiliario")

    # --- GRÁFICO 1: Dispersión geográfica por precio ---
    st.subheader("Ubicación geográfica y precios")

    fig_geo = px.scatter(
        df,
        x="lon",
        y="lat",
        color="precio",
        hover_data=["titulo", "ubicacion", "precio", "precio_m2", "habitaciones", "baños", "superficie_construida", "conservacion"],
        title="Distribución geográfica de precios de alquiler",
        labels={"lon": "Longitud", "lat": "Latitud", "precio": "Precio (€)"},
        color_continuous_scale="Viridis"
    )

    st.plotly_chart(fig_geo, use_container_width=True)

    # --- GRÁFICO 2: Boxplot por zona ---
    st.subheader("Distribución de Precios por Zona")

    fig_box = px.box(
        df,
        x="ubicacion",
        y="precio",
        points="outliers",
        hover_data=["titulo", "precio", "habitaciones", "baños", "superficie_construida"],
        labels={"ubicacion": "Zona", "precio": "Precio (€)"},
        title="Variabilidad de precios por zona"
    )

    fig_box.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_box, use_container_width=True)

    # --- DESCRIPCIÓN ---
    st.markdown("""
    Estos gráficos permiten al usuario:
    - 📍 Ver sobre el mapa cómo varía el precio por ubicación.
    - 📦 Detectar zonas con precios atípicos o muy variables.
    - ℹ️ Comparar inmuebles con info útil como superficie, habitaciones y estado.
    """)
