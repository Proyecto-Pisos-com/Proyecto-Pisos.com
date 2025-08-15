import streamlit as st
from PIL import Image
import base64

def show_landing_page():
    # Fondo crema global
    st.markdown("""
        <style>
            html, body, .main, .block-container {
                background-color: #fef6e4 !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Logo centrado
    def get_base64_logo(path):
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()

    logo_base64 = get_base64_logo("E:\Proyecto Final Bootcamp - copia\App Pisos.com Presentacion Final\data\pisos_logo.PNG")

    st.markdown(f"""
        <div style='text-align: center;'>
            <img src='data:image/png;base64,{logo_base64}' width='130'/>
        </div>
    """, unsafe_allow_html=True)

    # Subtítulo centrado
    st.markdown("""
    <div style='text-align:center; margin-top: 0.5rem; font-size:16px;'>
        Descubre inmuebles en <strong>Madrid</strong>, compara precios, analiza zonas y obtén valoraciones al instante.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # 🔍 ¿Qué puedes hacer? — imagen a la izquierda, texto a la derecha
    col1, col2 = st.columns([1, 1.4])
    with col1:
        st.image("E:\Proyecto Final Bootcamp - copia\App Pisos.com Presentacion Final\data\imagen_para_piso.PNG", width=390)
    with col2:
        st.markdown("""
        <h3>🔍 ¿Qué puedes hacer en esta app?</h3>
        <ul>
            <li>🏠 <strong>Buscar inmuebles</strong> en toda la ciudad de Madrid</li>
            <li>📍 <strong>Analizar zonas y precios</strong> por barrio</li>
            <li>🧠 <strong>Predecir el valor de un inmueble</strong> con modelos inteligentes</li>
            <li>🗺️ <strong>Visualizar en mapa</strong> y moverte por zonas fácilmente</li>
            <li>🆚 <strong>Comparar dos inmuebles</strong> antes de decidir</li>
        </ul>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ✅ Beneficios clave 
    col3, col4 = st.columns([1, 1.4])
    with col3:
        st.image(r"E:\Proyecto Final Bootcamp - copia\App Pisos.com Presentacion Final\data\beneficios.PNG", width=390)
    with col4:
        st.markdown("""
        <h3>✅ Beneficios clave</h3>
        <ul>
            <li>Sin necesidad de registro</li>
            <li>Acceso inmediato a inmuebles actualizados</li>
            <li>Completamente interactiva y visual</li>
            <li>Datos en <strong>tiempo real</strong></li>
            <li>Inspirada en la experiencia de usuario de <a href="https://www.pisos.com" target="_blank">pisos.com</a></li>
        </ul>
        """, unsafe_allow_html=True)

    # Pie de página
    st.markdown("---")
    st.markdown("📌 Usa el menú lateral izquierdo para comenzar", unsafe_allow_html=True)
