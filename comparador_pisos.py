import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

st.title("Comparador de Pisos: Gráfico Radar")

@st.cache_data
def cargar_datos():
    df = pd.read_csv("C:/Users/pablo/data/venta_madrid_modelado.csv")

    # Limpiar columnas que contienen textos tipo "230 m²"
    df["superficie_construida"] = df["superficie_construida"].astype(str).str.replace(" m²", "", regex=False)
    df["superficie_construida"] = pd.to_numeric(df["superficie_construida"], errors="coerce")
    df["metros"] = pd.to_numeric(df["metros"], errors="coerce")
    df["precio"] = pd.to_numeric(df["precio"], errors="coerce")
    return df

df = cargar_datos()

# Obtener lista de títulos únicos
pisos_disponibles = df["titulo"].dropna().unique()

if len(pisos_disponibles) < 2:
    st.warning("No hay suficientes pisos para comparar.")
else:
    piso1 = st.selectbox("Selecciona el primer piso", pisos_disponibles)
    piso2 = st.selectbox("Selecciona el segundo piso", [p for p in pisos_disponibles if p != piso1])

    # Filtrar los dos pisos seleccionados
    df_seleccion = df[df["titulo"].isin([piso1, piso2])][["titulo", "precio", "metros"]]

    if len(df_seleccion) < 2:
        st.warning("No se pudieron cargar correctamente los dos pisos.")
    else:
        df_seleccion = df_seleccion.fillna(0)  # Rellenar con 0 si falta algún valor

        # Escalar los datos para comparar en el radar
        scaler = MinMaxScaler()
        datos_escalados = scaler.fit_transform(df_seleccion[["precio", "metros"]])
        scaled_df = pd.DataFrame(datos_escalados, columns=["precio", "metros"])
        scaled_df["titulo"] = df_seleccion["titulo"].values

        # Configurar gráfico radar
        labels = ["precio", "metros"]
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        for _, row in scaled_df.iterrows():
            values = row[labels].tolist()
            values += values[:1]
            ax.plot(angles, values, label=row["titulo"])
            ax.fill(angles, values, alpha=0.25)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        ax.set_title("Comparación Precio vs Metros")
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

        st.pyplot(fig)
        


