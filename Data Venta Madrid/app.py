import streamlit as st
from data_page import show_data_page
from detail_page import show_detail_page
from charts_page import show_charts_page

st.set_page_config(
    page_title="Pisos.com - Venta",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("🔍 Navegación")
page = st.sidebar.radio("Selecciona una sección:", ["Inicio", "Datos", "Detalle", "Gráficos"])

def show_home_page():
    st.title("🏠 Bienvenido a Pisos.com - Venta")
    st.write("Explora los mejores inmuebles en venta en Madrid.")
    
    st.image(
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8FFOnmb-5Uu_oDIh0ZSOZAXBJiXrh7ihlTg&s",
        width=400
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
st.sidebar.markdown("📌 **Proyecto Final Bootcamp** - Pisos.com Venta")

