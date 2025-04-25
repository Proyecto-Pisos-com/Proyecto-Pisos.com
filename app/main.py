import sys
import os
import streamlit as st

# Aseguramos que Python entienda la carpeta raíz para imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Importar módulos de páginas
from app.landing_page import show_landing_page
from app.data_page import show_data_page
from app.detail_page import show_detail_page
from app.tabla_detallada import show_tabla_detallada_page

from alquiler.dispersion import show_dispersion
from alquiler.coropletico import show_coropletico
from alquiler.ficha_inmueble import show_ficha_inmueble
from alquiler.graficos_extra import show_graficos_extra
from alquiler.graficos_mercado import show_graficos_mercado

from comparador.comparador_alquiler import show_comparador_alquiler
from comparador.comparador_pisos import show_comparador_pisos

from coordenadas.mapa_coropletico_barrios import show_mapa_coropletico_barrios
from coordenadas.mapa_interactivo import show_mapa_interactivo

from venta.archivos_graficas import show_archivos_graficas
from venta.charts_page import show_charts_page
from venta.grafico_dispersion import show_grafico_dispersion
from venta.grafico_distribucion_precios import show_grafico_distribucion_precios

# Configuración de la app
st.set_page_config(
    page_title="Pisos.com",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Selector general de Alquiler o Venta
if "modo" not in st.session_state:
    st.session_state.modo = "alquiler"  # por defecto

modo = st.sidebar.selectbox("📂 Selecciona tipo de análisis:", ["Alquiler", "Venta"])
st.session_state.modo = "alquiler" if modo == "Alquiler" else "venta"

# Navegación lateral
if st.session_state.modo == "alquiler":
    pagina = st.sidebar.radio("Navegación - Alquiler:", [
        "Landing Page",
        "Datos",
        "Detalle",
        "Tabla Detallada",
        "Dispersion",
        "Coroplético",
        "Ficha Inmueble",
        "Gráficos Extra",
        "Gráficos Mercado",
        "Comparador Alquiler",
        "Mapa Interactivo"
    ])
else:
    pagina = st.sidebar.radio("Navegación - Venta:", [
        "Landing Page",
        "Archivos Gráficas",
        "Gráficos Interactivos Venta",
        "Gráfico Dispersión Venta",
        "Distribución Precios Venta",
        "Comparador Pisos Venta",
        "Mapa Coroplético Barrios"
    ])

# Mostrar página según navegación
if pagina == "Landing Page":
    show_landing_page()

elif pagina == "Datos":
    show_data_page()

elif pagina == "Detalle":
    show_detail_page()

elif pagina == "Tabla Detallada":
    show_tabla_detallada_page()

elif pagina == "Dispersion":
    show_dispersion()

elif pagina == "Coroplético":
    show_coropletico()

elif pagina == "Ficha Inmueble":
    show_ficha_inmueble()

elif pagina == "Gráficos Extra":
    show_graficos_extra()

elif pagina == "Gráficos Mercado":
    show_graficos_mercado()

elif pagina == "Comparador Alquiler":
    show_comparador_alquiler()

elif pagina == "Mapa Interactivo":
    show_mapa_interactivo()

elif pagina == "Archivos Gráficas":
    show_archivos_graficas()

elif pagina == "Gráficos Interactivos Venta":
    show_charts_page()

elif pagina == "Gráfico Dispersión Venta":
    show_grafico_dispersion()

elif pagina == "Distribución Precios Venta":
    show_grafico_distribucion_precios()

elif pagina == "Comparador Pisos Venta":
    show_comparador_pisos()

elif pagina == "Mapa Coroplético Barrios":
    show_mapa_coropletico_barrios()

# Pie de página
st.sidebar.markdown("---")
st.sidebar.markdown("📌 Proyecto Pisos.com - Análisis Alquiler y Venta")
