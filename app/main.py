import sqlite3
import pandas as pd
import sys
import os
import streamlit as st

# Añadir carpeta raíz al path para permitir imports relativos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# --- Importar funciones de páginas ---
from app.landing_page import show_landing_page
from app.data_page import show_data_page
from app.detail_page import show_detail_page
from app.utils import set_background_color

from bases_de_datos.app_streamlit_sql import show_sql_explorer
from Equipo.about_us import show_about_us

from machine_learning.detector_piso import show_deal_detector
from machine_learning.redes_neuronales import show_redes_neuronales
from machine_learning.calculadora_compra import show_calculadora_compra

from alquiler.tabla_detallada import show_tabla_detallada_page  
from alquiler.dispersion import show_dispersion
from alquiler.analisis_zona import show_coropletico
from alquiler.graficos_extra import show_graficos_extra
from alquiler.graficos_mercado import show_graficos_mercado

from comparador.comparador_alquiler import show_comparador_alquiler
from comparador.comparador_pisos import show_comparador_pisos

from coordenadas.mapa_interactivo import show_mapa_interactivo

from venta.charts_page import show_charts_page
from venta.grafico_distribucion_precios import show_grafico_distribucion_precios


# --- Configuración general de la app ---
st.set_page_config(
    page_title="Pisos.com",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

set_background_color()

# Estado inicial del modo
if "modo" not in st.session_state:
    st.session_state.modo = "alquiler"

# --- Selector principal (ordenado: Venta primero) ---
modo = st.sidebar.selectbox(
    "📂 Selecciona tipo de análisis:",
    ["Venta", "Alquiler", "Base de Datos", "Redes Neuronales", "About Us"],
    key="modo_selector"
)

st.session_state.modo = (
    "venta" if modo == "Venta"
    else "alquiler" if modo == "Alquiler"
    else "base_datos" if modo == "Base de Datos"
    else "redes_neuronales" if modo == "Redes Neuronales"
    else "about_us"
)

# --- Mostrar Base de Datos ---
if st.session_state.modo == "base_datos":
    show_sql_explorer()

# --- Menú de navegación: ALQUILER ---
elif st.session_state.modo == "alquiler":
    pagina = st.sidebar.radio("Navegación - Alquiler:", [
        "Inicio",
        "Tabla Detallada",
        "Dispersion",
        "Análisis por Zona",
        "Gráficos Extra",
        "Gráficos Mercado",
        "Comparador Alquiler",
        "Mapa Interactivo",
        "Detector de Chollos",
    ])

    if pagina == "Inicio":
        show_landing_page()
    elif pagina == "Tabla Detallada":
        show_tabla_detallada_page()
    elif pagina == "Dispersion":
        show_dispersion()
    elif pagina == "Análisis por Zona":
        show_coropletico()
    elif pagina == "Gráficos Extra":
        show_graficos_extra()
    elif pagina == "Gráficos Mercado":
        show_graficos_mercado()
    elif pagina == "Comparador Alquiler":
        show_comparador_alquiler()
    elif pagina == "Mapa Interactivo":
        show_mapa_interactivo()
    elif pagina == "Detector de Chollos":
        show_deal_detector()

# --- Menú de navegación: VENTA ---
elif st.session_state.modo == "venta":
    pagina = st.sidebar.radio("Navegación - Venta:", [
        "Inicio",
        "Analiza tu inmueble",
        "Calcula tu compra",
        "Compara tu futuro piso",
        "Distribución de los precios"
    ])

    if pagina == "Inicio":
        show_landing_page()
    elif pagina == "Analiza tu inmueble":
        show_charts_page()
    elif pagina == "Calcula tu compra":
        show_calculadora_compra()
    elif pagina == "Compara tu futuro piso":
        show_comparador_pisos()
    elif pagina == "Distribución de los precios":
        show_grafico_distribucion_precios()

# --- Página: Redes Neuronales ---
elif st.session_state.modo == "redes_neuronales":
    show_redes_neuronales()

# --- Página: About Us ---
elif st.session_state.modo == "about_us":
    show_about_us()

# --- Pie de página ---
st.sidebar.markdown("---")
st.sidebar.markdown("📌 Proyecto Pisos.com - Análisis Alquiler y Venta")
