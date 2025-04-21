import streamlit as st
import pandas as pd
import plotly.express as px
import os

def show_charts_page():
    """ Vista de gráficos interactivos sobre alquiler de inmuebles. """
    
    st.title("📈 Análisis de Alquileres en Madrid")

    csv_path = r"E:\Proyecto Final Bootcamp - copia\Proyecto Final\Pisos.com\Proyecto speed 1\Data Alquiler Unificado\alquiler_unificado_con_coordenadas_unicos.csv"

    if not os.path.exists(csv_path):
        st.error(f"⚠️ Archivo CSV no encontrado en la ruta: {csv_path}")
        return

    data = pd.read_csv(csv_path)

    if "precio_num" in data.columns:
        st.subheader("💰 Distribución de Precios de Alquiler")
        fig_precio = px.histogram(data, x="precio_num", nbins=50, title="Distribución de Precios de Alquiler")
        st.plotly_chart(fig_precio)
    else:
        st.warning("⚠️ La columna 'precio_num' no existe en el archivo CSV.")

    if {"habitaciones_num", "precio_num"}.issubset(data.columns):
        st.subheader("🏠 Relación Habitaciones vs Precio")
        fig_habitaciones = px.scatter(data, x="habitaciones_num", y="precio_num", title="Habitaciones vs Precio", trendline="ols")
        st.plotly_chart(fig_habitaciones)
    else:
        st.warning("⚠️ No se encontraron las columnas necesarias.")

    if {"lat", "lon"}.issubset(data.columns):
        st.subheader("📍 Ubicación de los Inmuebles en Alquiler")
        fig_map = px.scatter_mapbox(data, lat="lat", lon="lon", hover_name="titulo_y",
                                    color="precio_num", title="Mapa de Alquileres",
                                    zoom=12, height=500)
        fig_map.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig_map)
    else:
        st.warning("⚠️ No se encontraron coordenadas.")
