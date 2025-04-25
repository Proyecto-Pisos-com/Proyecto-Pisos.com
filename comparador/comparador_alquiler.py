import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
from utils import cargar_datos

def show_comparador_alquiler():
    st.title("🕹️ Comparador de Inmuebles de Alquiler")

    # --- Cargar datos ---
    @st.cache_data
    def cargar_filtrados():
        df = cargar_datos("alquiler.csv")
        return df

    df = cargar_filtrados()

    # --- Detectar columnas numéricas útiles ---
    variables_numericas = df.select_dtypes(include=["float64", "int64"]).columns
    variables_excluidas = ["lat", "lon"]
    variables = [v for v in variables_numericas if v not in variables_excluidas]

    # --- Verificar títulos únicos ---
    titulos = df["titulo"].dropna().unique().tolist()
    if len(titulos) < 2:
        st.warning("No hay suficientes inmuebles únicos para comparar.")
        st.stop()

    # --- Selección de inmuebles ---
    titulo_1 = st.selectbox("Selecciona el primer inmueble", options=titulos, key="inm1_alq")
    titulo_2 = st.selectbox("Selecciona el segundo inmueble", options=[t for t in titulos if t != titulo_1], key="inm2_alq")

    # --- Filtrar y verificar ---
    df_comp = df[df["titulo"].isin([titulo_1, titulo_2])].copy()
    if df_comp.shape[0] < 2:
        st.warning("No se encontraron datos suficientes para ambos inmuebles.")
        st.stop()

    # --- Tabla comparativa real ---
    st.subheader("📊 Comparativa de valores reales")

    inm1_vals = df_comp[df_comp["titulo"] == titulo_1][variables].iloc[0]
    inm2_vals = df_comp[df_comp["titulo"] == titulo_2][variables].iloc[0]

    comparacion = pd.DataFrame({
        "Variable": variables,
        titulo_1: [inm1_vals[v] for v in variables],
        titulo_2: [inm2_vals[v] for v in variables],
        "Diferencia absoluta": [abs(inm1_vals[v] - inm2_vals[v]) for v in variables]
    })

    st.dataframe(comparacion.set_index("Variable"), use_container_width=True)

    # --- Normalizar para gráfico radar ---
    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df_comp[variables]), columns=variables)
    df_scaled["titulo"] = df_comp["titulo"].values

    # --- Gráfico radar ---
    fig = px.line_polar(
        df_scaled.melt(id_vars="titulo"),
        r="value",
        theta="variable",
        color="titulo",
        line_close=True,
        title="Comparación Visual Normalizada",
        color_discrete_map={titulo_1: "red", titulo_2: "blue"}
    )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        font=dict(size=14)
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- Explicación final ---
    st.markdown("""
    Este comparador muestra **todas las variables numéricas disponibles**, incluyendo:
    - Precio
    - Superficie
    - Habitaciones
    - Antigüedad
    - Y más si están en el dataset

    Puedes identificar claramente cuál de los dos inmuebles destaca en cada dimensión y por cuánto difiere.
    """)
