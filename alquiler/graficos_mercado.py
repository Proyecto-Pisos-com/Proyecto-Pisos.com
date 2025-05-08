import streamlit as st
import pandas as pd
import plotly.express as px
from utils import cargar_datos
from config import ALQUILER_CSV  

def show_graficos_mercado():
    # --- Cargar datos ---
    @st.cache_data
    def cargar_filtrados():
        df = cargar_datos(ALQUILER_CSV)  
        return df.dropna(subset=["precio", "superficie_construida", "ubicacion", "precio_m2"])

    df = cargar_filtrados()

    st.title("📊 Análisis del Mercado Inmobiliario por Zona")

    # --- FILTROS EN SIDEBAR ---
    st.sidebar.header("🔎 Filtros interactivos")

    # Rango de precios
    min_precio = int(df["precio"].min())
    max_precio = int(df["precio"].max())
    precio_range = st.sidebar.slider("Rango de precios (€)", min_precio, max_precio, (min_precio, max_precio))
    df = df[(df["precio"] >= precio_range[0]) & (df["precio"] <= precio_range[1])]

    # Filtro por zona
    zonas = sorted(df["ubicacion"].dropna().unique())
    zona_sel = st.sidebar.selectbox("Filtrar por zona (opcional)", ["Todas"] + zonas)
    if zona_sel != "Todas":
        df = df[df["ubicacion"] == zona_sel]

    # --- HISTOGRAMA DE PRECIOS ---
    st.subheader("Distribución de Precios de Alquiler")
    fig_hist = px.histogram(
        df,
        x="precio",
        nbins=50,
        title="Distribución de Precios de Alquiler",
        labels={"precio": "Precio (€)"}
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    # --- DISPERSIÓN PRECIO M2 vs SUPERFICIE Y RANKING ---
    st.subheader("Comparativa de Precio por Metro Cuadrado y Zona")

    col1, col2 = st.columns(2)

    with col1:
        fig_disp = px.scatter(
            df,
            x="superficie_construida",
            y="precio_m2",
            color="ubicacion",
            hover_data=["titulo", "precio", "habitaciones", "baños", "conservacion"],
            title="Precio por m² según Superficie y Zona",
            labels={
                "superficie_construida": "Superficie Construida (m²)",
                "precio_m2": "Precio por m² (€)",
                "ubicacion": "Zona"
            }
        )
        st.plotly_chart(fig_disp, use_container_width=True)

    with col2:
        st.subheader("🏅 Ranking de Zonas por Precio Medio por m²")

        ranking = df.groupby("ubicacion")["precio_m2"].agg(["count", "mean", "min", "max"]).round(2)
        ranking = ranking.rename(columns={
            "count": "Número de inmuebles",
            "mean": "Precio medio por m² (€)",
            "min": "Precio mínimo por m² (€)",
            "max": "Precio máximo por m² (€)"
        }).sort_values(by="Precio medio por m² (€)", ascending=False)

        st.dataframe(ranking, use_container_width=True)

    # --- NOTA FINAL ---
    st.markdown("""
    Esta herramienta te permite:
    - Explorar zonas con mayor o menor coste por metro cuadrado.
    - Ver la distribución de precios filtrando por tu presupuesto.
    - Comparar zonas directamente en una tabla ordenable.

    ✅ Consejo: usa los filtros laterales para ajustar los datos a tu criterio de búsqueda.
    """)
