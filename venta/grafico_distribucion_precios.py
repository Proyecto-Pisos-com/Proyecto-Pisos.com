import plotly.express as px
import pandas as pd
import streamlit as st
from utils import cargar_datos

def show_grafico_distribucion_precios():
    # --- Cargar datos ---
    @st.cache_data
    def cargar_filtrados():
        return cargar_datos("ventas.csv")

    df = cargar_filtrados()

    # --- Crear gráfico de histograma ---
    st.title("📊 Distribución de los Precios de los Inmuebles en Venta")

    fig = px.histogram(
        df, 
        x="precio", 
        nbins=30,
        title="Distribución de los Precios de los Inmuebles",
        labels={"precio": "Precio (€)"}
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- Descripción ---
    st.markdown("""
    Este gráfico muestra la **distribución de los precios** de los inmuebles en el mercado. 
    El eje X representa el rango de precios en euros, mientras que el eje Y muestra el número de inmuebles que caen dentro de cada rango de precios. 

    📌 **Interpretación**:
    - Entender los precios más frecuentes.
    - Detectar si hay zonas de precios anormalmente altos o bajos.
    """)
