import streamlit as st
from data_page import show_data_page
from detail_page import show_detail_page
from charts_page import show_charts_page

st.set_page_config(
    page_title="Pisos.com - Alquiler",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("🔍 Navegación")
page = st.sidebar.radio("Selecciona una sección:", ["Inicio", "Datos", "Detalle", "Gráficos"])

def show_home_page():
    st.title("🏠 Bienvenido a Pisos.com - Alquiler")
    st.write("Explora los mejores inmuebles en alquiler en Madrid.")
    
    # Imagen central principal
    st.image( 
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8FFOnmb-5Uu_oDIh0ZSOZAXBJiXrh7ihlTg&s",
        width=400
    )

    # Crear un diseño para imágenes inclinadas usando columnas
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.markdown(
            """
            <div style="transform: rotate(-45deg);">
                <img src="https://fotos.imghs.net/media/pisosblog/2018/06/7-ideas-para-separar-ambientes-con-telas2.jpg" width="200" />
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div style="transform: rotate(45deg);">
                <img src="https://fotos.imghs.net/mm-wp/1018/518/1018_106354518_1_2025041412044131826.jpg" width="200" />
            </div>
            """,
            unsafe_allow_html=True
        )

    # Imagen central inferior
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i0.wp.com/www.pulido-de-pisos.com/wp-content/uploads/2023/08/pisos-para-interiores.jpg" width="300" />
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Nueva fila para las imágenes adicionales
    col4, col5 = st.columns([1, 1])

    with col4:
        st.image(
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSLxcjtm35XSlMTeK72cCBn-FSGk_DUUexGzQ&s",
            width=300
        )

    with col5:
        st.image(
            "https://fotos.imghs.net/mm-wp/1093/618/1093_EP951-2618_1_2025040105363131250.jpg",
            width=300
        )

if page == "Inicio":
    show_home_page()
elif page == "Datos":
    show_data_page()
elif page == "Detalle":
    show_detail_page()
elif page == "Gráficos":
    show_charts_page()

st.sidebar.markdown("---")
st.sidebar.markdown("📌 **Proyecto Final Bootcamp** - Pisos.com Alquiler")
