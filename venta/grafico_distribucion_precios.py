import plotly.express as px
import pandas as pd
import streamlit as st
from utils import cargar_datos
from config import VENTAS_CSV

def show_grafico_distribucion_precios():
    # --- Cargar datos ---
    @st.cache_data
    def cargar_filtrados():
        return cargar_datos(VENTAS_CSV)

    df = cargar_filtrados()

    # --- Crear tipo_vivienda desde columnas booleanas ---
    lista_tipos_vivienda = ["piso", "atico", "estudio", "apartamento", "duplex", "chalet", "finca", "loft"]
    columnas_presentes = [col for col in lista_tipos_vivienda if col in df.columns]

    if columnas_presentes:
        df["tipo_vivienda"] = df[columnas_presentes].to_numpy().argmax(axis=1)
        df["tipo_vivienda"] = df["tipo_vivienda"].apply(lambda val: columnas_presentes[val].capitalize())
    else:
        df["tipo_vivienda"] = "Sin Categoría"

    df = df[df["tipo_vivienda"] != "Sin Categoría"]

    # --- Filtro por precio máximo ---
    st.title("📊 Análisis de Precios de Inmuebles en Venta")
    max_precio = int(df["precio"].quantile(0.95))
    precio_max = st.slider("Filtrar por precio máximo (€)", min_value=50000, max_value=max_precio * 2, value=max_precio, step=10000)
    df_filtrado = df[df["precio"] <= precio_max]

    # --- Colores por tipo de vivienda ---
    color_map = {
        "Piso": "#d62728", "Casa": "#ff7f0e", "Ático": "#17becf", "Estudio": "#1f77b4",
        "Apartamento": "#9467bd", "Dúplex": "#8c564b", "Chalet": "#e377c2",
        "Finca": "#7f7f7f", "Loft": "#2ca02c", "Sin Categoría": "#999999"
    }

    # --- HISTOGRAMA: distribución de precios ---
    st.subheader("📉 Distribución de Precios")
    fig_hist = px.histogram(
        df_filtrado,
        x="precio",
        nbins=30,
        color="tipo_vivienda",
        color_discrete_map=color_map,
        labels={"precio": "Precio (€)"},
        title="Distribución de los Precios de los Inmuebles"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    # --- DISPERSIÓN y BOXPLOT en dos columnas ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Precio vs. Superficie Construida")
        fig_dispersion = px.scatter(
            df_filtrado,
            x="superficie_construida",
            y="precio",
            color="tipo_vivienda",
            color_discrete_map=color_map,
            labels={"superficie_construida": "Superficie Construida (m²)", "precio": "Precio (€)"},
            title="Relación entre Precio y Tamaño por Tipo de Vivienda"
        )
        st.plotly_chart(fig_dispersion, use_container_width=True)

    with col2:
        st.subheader("📦 Boxplot por Tipo de Vivienda")
        fig_box = px.box(
            df_filtrado,
            x="tipo_vivienda",
            y="precio",
            color="tipo_vivienda",
            color_discrete_map=color_map,
            labels={"tipo_vivienda": "Tipo de Vivienda", "precio": "Precio (€)"},
            title="Rango de Precios por Tipo de Inmueble"
        )
        st.plotly_chart(fig_box, use_container_width=True)

    # --- Explicación ---
    with st.expander("🧠 Interpretación y conclusiones"):
        st.markdown("""
        - El **histograma** te permite ver la concentración de precios en el mercado.
        - La **dispersión** muestra cómo influye la superficie en el precio según tipo de vivienda.
        - El **boxplot** compara rangos y medianas de precios entre distintos tipos de inmuebles.

        💡 Puedes usar el filtro superior para excluir valores extremos y centrarte en el mercado real.
        """)
