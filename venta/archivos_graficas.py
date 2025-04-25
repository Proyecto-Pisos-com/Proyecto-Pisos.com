import plotly.express as px
import pandas as pd
import streamlit as st
from utils import cargar_datos

def show_archivos_graficas():
    # --- Cargar datos ---
    @st.cache_data
    def cargar_filtrados():
        df = cargar_datos("ventas.csv")
        return df

    df = cargar_filtrados()

    # --- Crear nueva columna combinada de tipo de vivienda ---
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

    # --- Gráfico de dispersión: Precio vs Superficie Útil ---
    st.title("📈 Relación Precio vs Superficie Útil en Ventas")

    fig1 = px.scatter(
        df, 
        x="superficie_util",  
        y="precio",           
        color="tipo_vivienda",  
        labels={"superficie_util": "Superficie Útil (m²)", "precio": "Precio (€)"},
        title="Relación entre Precio y Superficie Útil"
    )

    st.plotly_chart(fig1)

    # --- Descripción ---
    st.markdown("""
    Este gráfico de **dispersión** muestra la relación entre el **precio** de los inmuebles y su **superficie útil**. 
    El eje X representa la superficie útil de los inmuebles, mientras que el eje Y muestra el precio en euros. 
    Cada punto está coloreado según el **tipo de vivienda**, lo que permite observar cómo varían los precios según la superficie útil.
    """)
