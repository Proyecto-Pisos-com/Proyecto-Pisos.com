import streamlit as st
from landing_page import show_landing_page
from data_page import show_data_page
from detail_page import show_detail_page

# Configuración de Streamlit
st.set_page_config(
    page_title="Pisos.com",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Encabezado con el logo a la izquierda y botones en la derecha
st.markdown("""
    <style>
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            background-color: #f1f1f1;
        }
        .logo {
            width: 120px;
        }
        .title {
            text-align: center;
            font-size: 24px;
            color: #007BFF;
            margin: 0 auto;
        }
        .buttons {
            display: flex;
            gap: 10px;
        }
        .button {
            font-size: 16px;
            text-decoration: none;
            font-weight: bold;
            color: #007BFF;
            border: 2px solid #007BFF;
            padding: 5px 10px;
            border-radius: 5px;
            text-align: center;
        }
        .button:hover {
            background-color: #eaeaea;
        }
    </style>
    <div class="header-container">
        <!-- Logo en la esquina superior izquierda -->
        <img class="logo" src="https://cdn-tecnocasagroup.medialabtc.it/es/2019/01/logo_pisos.com_.png" alt="Logo Pisos.com">
        <!-- Título principal centrado -->
        <div class="title">Explora los mejores pisos</div>
        <!-- Botones en la esquina superior derecha -->
        <div class="buttons">
            <a href="#" class="button">Inscribirse</a>
            <a href="#" class="button">Iniciar sesión</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Espaciado entre el encabezado y el contenido principal
st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# Contenido principal centrado
st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <h2 style="color: #007BFF;">Encuentra tu lugar ideal con Pisos.com</h2>
    </div>
    """, unsafe_allow_html=True)

# Barra lateral para la navegación
st.sidebar.title("Navegación")
page = st.sidebar.radio("Selecciona una sección:", ["Landing Page", "Datos", "Detalle"])

# Lógica de navegación
if page == "Landing Page":
    show_landing_page()
elif page == "Datos":
    show_data_page()
elif page == "Detalle":
    show_detail_page()

