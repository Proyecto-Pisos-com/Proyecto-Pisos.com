import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

st.set_page_config(page_title="Comparador Dinámico de Pisos", layout="centered")
st.title("📊 Comparador Dinámico de Pisos en Alquiler")

@st.cache_data
def cargar_datos():
    df = pd.read_json("alquiler_comparador_limpio.json", orient="table")
    return df

df = cargar_datos()

# Extraer nombres de pisos y columnas numéricas
pisos = df.index.tolist()
columnas_numericas = df.select_dtypes(include=np.number).columns.tolist()

# Sidebar de selección
st.sidebar.header("Opciones de comparación")

piso1 = st.sidebar.selectbox("🏠 Selecciona el primer piso", pisos)
piso2 = st.sidebar.selectbox("🏠 Selecciona el segundo piso", [p for p in pisos if p != piso1])

columnas_seleccionadas = st.sidebar.multiselect(
    "📌 Selecciona variables a comparar",
    columnas_numericas,
    default=columnas_numericas[:3]  # Selección por defecto
)

if len(columnas_seleccionadas) < 2:
    st.warning("Selecciona al menos 2 variables para comparar.")
else:
    df_comp = df.loc[[piso1, piso2], columnas_seleccionadas]

    # --- GRÁFICO RADAR ---
    scaler = MinMaxScaler()
    datos_escalados = scaler.fit_transform(df_comp)
    scaled_df = pd.DataFrame(datos_escalados, columns=columnas_seleccionadas, index=[piso1, piso2])

    angles = np.linspace(0, 2 * np.pi, len(columnas_seleccionadas), endpoint=False).tolist()
    angles += angles[:1]

    fig_radar, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    for nombre, fila in scaled_df.iterrows():
        valores = fila.tolist() + [fila.tolist()[0]]
        ax.plot(angles, valores, label=nombre)
        ax.fill(angles, valores, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(columnas_seleccionadas)
    ax.set_title("Comparación Radar")
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    st.pyplot(fig_radar)

    # --- GRÁFICO DE BARRAS ---
    st.subheader("Comparación Numérica Real")
    fig_bar, ax_bar = plt.subplots()
    df_comp.T.plot(kind="bar", ax=ax_bar)
    ax_bar.set_ylabel("Valor")
    ax_bar.set_title("Comparación directa por variable")
    ax_bar.legend(title="Piso")
    st.pyplot(fig_bar)


