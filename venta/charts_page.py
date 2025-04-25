import streamlit as st
import pandas as pd
import plotly.express as px
from utils import cargar_datos

def show_charts_page():
    """ Vista de gráficos interactivos sobre ventas de inmuebles. """
    
    st.title("📈 Análisis de Ventas de Inmuebles en Madrid")

    # --- Cargar datos ---
    @st.cache_data
    def cargar_filtrados():
        return cargar_datos("ventas.csv")

    df = cargar_filtrados()

    # Verificar si hay datos cargados
    if df.empty:
        st.error("⚠️ No se pudo cargar el archivo de ventas.")
        return

    # --- Verificar columnas y mostrar gráficos ---

    if "precio" in df.columns:
        st.subheader("💰 Distribución de Precios de Venta")
        fig_precio = px.histogram(df, x="precio", nbins=50, title="Distribución de Precios de Venta")
        st.plotly_chart(fig_precio, use_container_width=True)
    else:
        st.warning("⚠️ La columna 'precio' no existe en el archivo CSV.")

    if {"habitaciones", "precio"}.issubset(df.columns):
        st.subheader("🏠 Relación Habitaciones vs Precio")
        fig_habitaciones = px.scatter(df, x="habitaciones", y="precio", title="Habitaciones vs Precio", trendline="ols")
        st.plotly_chart(fig_habitaciones, use_container_width=True)
    else:
        st.warning("⚠️ No se encontraron las columnas necesarias para el gráfico de habitaciones.")

    if {"lat", "lon"}.issubset(df.columns):
        st.subheader("📍 Ubicación de los Inmuebles")
        fig_map = px.scatter_mapbox(
            df, 
            lat="lat", 
            lon="lon", 
            hover_name="titulo",
            color="precio",
            title="Mapa de Precios de Inmuebles en Venta",
            zoom=12,
            height=500
        )
        fig_map.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("⚠️ No se encontraron coordenadas para el mapa.")

    st.markdown("""
    Esta página proporciona un análisis visual de los precios de venta de inmuebles en Madrid. 
    - El histograma muestra cómo se distribuyen los precios en el mercado.
    - El gráfico de dispersión compara el número de habitaciones con el precio.
    - El mapa permite visualizar la distribución geográfica de los inmuebles según el precio.
    """)
