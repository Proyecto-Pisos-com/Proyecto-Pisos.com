import streamlit as st
import pandas as pd
import plotly.express as px
from utils import cargar_datos  # Asegúrate que utils.py esté en app/

def show_coropletico():
    st.title("🌐 Mapa Coroplético - Análisis por Zona")

    # Determinar si estamos en modo alquiler o ventas
    modo = st.session_state.get("modo", "alquiler")
    archivo = "alquiler.csv" if modo == "alquiler" else "ventas.csv"
    df = cargar_datos(archivo)

    if df.empty or "ubicacion" not in df.columns or "precio" not in df.columns:
        st.warning("No se pudieron cargar los datos necesarios.")
        return

    df_agrupado = df.groupby("ubicacion").agg(
        cantidad_inmuebles=("precio", "count"),
        precio_medio=("precio", "mean")
    ).reset_index()

    # Gráfico de barras - Cantidad
    st.subheader("Cantidad de inmuebles por zona")
    fig_cantidad = px.bar(
        df_agrupado.sort_values("cantidad_inmuebles", ascending=False),
        x="ubicacion", y="cantidad_inmuebles",
        labels={"ubicacion": "Zona", "cantidad_inmuebles": "Cantidad"},
        title="Cantidad de inmuebles por zona"
    )
    st.plotly_chart(fig_cantidad, use_container_width=True)

    # Gráfico de barras - Precio medio
    st.subheader("Precio medio de alquiler por zona")
    fig_precio = px.bar(
        df_agrupado.sort_values("precio_medio", ascending=False),
        x="ubicacion", y="precio_medio",
        labels={"ubicacion": "Zona", "precio_medio": "Precio medio (€)"},
        title="Precio medio de alquiler por zona"
    )
    st.plotly_chart(fig_precio, use_container_width=True)
