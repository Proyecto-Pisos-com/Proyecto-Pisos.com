import streamlit as st
import pandas as pd
import plotly.express as px
from utils import cargar_datos
from config import ALQUILER_CSV  

@st.cache_data
def cargar_filtrados():
    return cargar_datos(ALQUILER_CSV)  


def mostrar_grafico_barras(df, x_col, y_col, titulo, etiqueta_y, descripcion, color="blue", tipo="bar"):
    df = df.sort_values(y_col, ascending=False).head(30)  

    if tipo == "bar":
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            text_auto=True,
            labels={x_col: "Zona", y_col: etiqueta_y},
            title=titulo,
            color_discrete_sequence=[color]
        )
        fig.update_traces(textfont_size=12, marker_line_width=0.5)
    elif tipo == "line":
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            markers=True,
            labels={x_col: "Zona", y_col: etiqueta_y},
            title=titulo
        )
        fig.update_traces(line=dict(width=3), marker=dict(size=8))
    else:
        return  

    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(descripcion)


def show_coropletico():
    st.title("📊 Análisis por Zona - Distribución y Precios")

    df = cargar_filtrados()

    if df.empty or "ubicacion" not in df.columns or "precio" not in df.columns:
        st.warning("No se pudieron cargar los datos necesarios.")
        return

    # Agrupar por ubicación
    df_agrupado = df.groupby("ubicacion").agg(
        cantidad_inmuebles=("precio", "count"),
        precio_medio=("precio", "mean")
    ).reset_index()

    # Gráfico 1: Cantidad de inmuebles por zona
    st.subheader("Cantidad de inmuebles por zona")
    mostrar_grafico_barras(
        df_agrupado,
        x_col="ubicacion",
        y_col="cantidad_inmuebles",
        titulo="Cantidad de inmuebles por zona (Top 30)",
        etiqueta_y="Cantidad",
        descripcion="""
        📌 Este gráfico muestra el número total de inmuebles disponibles por zona (máx. 30 zonas con más oferta).
        Puede ayudarte a identificar las áreas con mayor presencia en el mercado.
        """,
        color="royalblue",
        tipo="bar"
    )

    # Gráfico 2: Precio medio por zona (como línea)
    st.subheader("Precio medio de venta por zona")
    mostrar_grafico_barras(
        df_agrupado,
        x_col="ubicacion",
        y_col="precio_medio",
        titulo="Precio medio de venta por zona (Top 30)",
        etiqueta_y="Precio medio (€)",
        descripcion="""
        💰 Este gráfico presenta el precio promedio de venta en las zonas más destacadas (top 30).
        Es útil para comparar niveles de precios y detectar áreas más exclusivas o asequibles.
        """,
        color="darkorange",
        tipo="line"
    )
