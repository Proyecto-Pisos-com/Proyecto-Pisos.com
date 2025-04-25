import streamlit as st

def show_landing_page():
    st.title("🏠 Bienvenido a Pisos.com")
    st.markdown("Explora los mejores pisos en **Madrid** para alquilar o comprar.")

    st.image(
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8FFOnmb-5Uu_oDIh0ZSOZAXBJiXrh7ihlTg&s",
        width=400
    )

    st.markdown("---")
    st.markdown("### ¿Qué puedes hacer en esta app?")
    st.markdown("""
    - 🔍 Consultar inmuebles disponibles.
    - 📊 Analizar precios y zonas.
    - 🧠 Estimar el valor de un alquiler.
    - 🗺️ Ver mapas interactivos.
    - ⚖️ Comparar dos inmuebles fácilmente.
    """)

    st.success("¡Empieza navegando con el menú de la izquierda!")
