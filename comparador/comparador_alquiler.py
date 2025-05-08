import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import cargar_datos
from config import ALQUILER_CSV  # ✅ Usamos la ruta desde config

def show_comparador_alquiler():
    st.title("🕹️ Comparador de Inmuebles de Alquiler")

    # --- Cargar datos ---
    @st.cache_data
    def cargar_filtrados():
        return cargar_datos(ALQUILER_CSV)  # ✅ Ruta centralizada

    df = cargar_filtrados()

    # --- Selección de inmuebles ---
    titulos = df["titulo"].dropna().unique().tolist()
    if len(titulos) < 2:
        st.warning("No hay suficientes inmuebles únicos para comparar.")
        return

    col1, col2 = st.columns([1, 1])
    with col1:
        titulo_1 = st.selectbox("Selecciona el primer inmueble", titulos, key="inm1")
    with col2:
        titulo_2 = st.selectbox("Selecciona el segundo inmueble", [t for t in titulos if t != titulo_1], key="inm2")

    df_comp = df[df["titulo"].isin([titulo_1, titulo_2])].copy()
    if df_comp.shape[0] < 2:
        st.warning("No hay suficientes datos.")
        return

    # --- Variables a comparar ---
    variables = ["precio", "habitaciones", "baños", "metros", "superficie_construida", "precio_m2"]
    variables = [v for v in variables if v in df_comp.columns]

    vals_1 = df_comp[df_comp["titulo"] == titulo_1][variables].iloc[0]
    vals_2 = df_comp[df_comp["titulo"] == titulo_2][variables].iloc[0]

    # --- Comparativa real ---
    st.subheader("📊 Comparativa de valores reales")
    comparacion = pd.DataFrame({
        "Variable": variables,
        titulo_1: [vals_1[v] for v in variables],
        titulo_2: [vals_2[v] for v in variables],
        "Diferencia absoluta": [abs(vals_1[v] - vals_2[v]) for v in variables]
    })
    st.dataframe(comparacion.set_index("Variable"), use_container_width=True)

    # --- Gráfico de valores reales (sin normalizar) ---
    st.markdown("### 📉 Comparación Visual de Valores Reales")
    col_graf, col_info = st.columns([2, 1])

    with col_graf:
        fig = go.Figure(data=[
            go.Bar(name=titulo_1, x=variables, y=[vals_1[v] for v in variables], marker_color="red"),
            go.Bar(name=titulo_2, x=variables, y=[vals_2[v] for v in variables], marker_color="blue")
        ])
        fig.update_layout(
            barmode="group",
            xaxis_title="Variable",
            yaxis_title="Valor",
            height=500,
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_info:
        st.markdown("### ℹ️ Interpreta el gráfico:")
        st.markdown("""
        Esta gráfica muestra los **valores reales** de cada inmueble en variables como:
        - **Precio**
        - **Superficie**
        - **Habitaciones**
        - Y más, según disponibilidad.

        Útil para una **comparación directa sin escalado ni normalización**.
        """)
