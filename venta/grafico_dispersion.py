import plotly.express as px
import pandas as pd
import streamlit as st
from utils import cargar_datos

def show_grafico_dispersion():
    # --- Cargar datos ---
    @st.cache_data
    def cargar_filtrados():
        return cargar_datos("ventas.csv")

    df = cargar_filtrados()

    # --- Crear columna de tipo de vivienda ---
    def asignar_tipo_vivienda(row):
        if row['piso']:
            return 'Piso'
        elif row['casa']:
            return 'Casa'
        elif row['atico']:
            return 'Ático'
        elif row['estudio']:
            return 'Estudio'
        elif row['apartamento']:
            return 'Apartamento'
        elif row['duplex']:
            return 'Dúplex'
        elif row['chalet']:
            return 'Chalet'
        elif row['finca']:
            return 'Finca'
        elif row['loft']:
            return 'Loft'
        else:
            return 'Sin Categoría'

    df['tipo_vivienda'] = df.apply(asignar_tipo_vivienda, axis=1)

    # --- Crear gráfico de dispersión ---
    st.title("📈 Relación entre Precio y Superficie Construida en Ventas")

    fig = px.scatter(
        df, 
        x="superficie_construida", 
        y="precio", 
        color="tipo_vivienda",
        labels={"superficie_construida": "Superficie Construida (m²)", "precio": "Precio (€)"},
        title="Relación entre Precio y Superficie Construida"
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- Descripción ---
    st.markdown("""
    Este gráfico de **dispersión** muestra la **relación entre el precio** de los inmuebles y su **superficie construida** en metros cuadrados. 
    El eje X representa la superficie construida de los inmuebles, mientras que el eje Y muestra el precio en euros. 
    Cada punto en el gráfico corresponde a un inmueble y está coloreado según el **tipo de vivienda**.

    ### **Interpretación del gráfico**:
    - Si existe una **correlación positiva**, deberíamos esperar ver que los inmuebles más grandes (con mayor superficie) tienden a tener precios más altos.
    - El gráfico permite identificar patrones, como si los precios de ciertas categorías de viviendas (por ejemplo, pisos o casas) tienden a variar más o menos según la superficie.
    """)

