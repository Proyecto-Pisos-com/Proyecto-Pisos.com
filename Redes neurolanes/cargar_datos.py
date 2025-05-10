import pandas as pd
import streamlit as st

@st.cache_data
def cargar_datos(nombre_archivo):
    """Carga el dataset desde un archivo CSV."""
    return pd.read_csv(nombre_archivo)

