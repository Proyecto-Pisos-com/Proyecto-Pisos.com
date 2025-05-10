import streamlit as st
from config import (
    FOTO_PABLO, FOTO_CARLA, FOTO_LUIS, FOTO_YONES,
    CV_PABLO
)

def show_about_us():
    st.title("👥 ¿ Quienes Somos ?")
    st.markdown("Esta sección contiene información sobre los integrantes del proyecto y sus perfiles profesionales.")
    st.markdown("---")

    def perfil(nombre, imagen, linkedin, github, cv=None, ancho_foto=100):
        st.image(imagen, width=ancho_foto)
        st.markdown(f"**{nombre}**")
        st.markdown("Estudiante y desarrollador de la app.")
        st.markdown(f"- 🔗 [LinkedIn]({linkedin})")
        st.markdown(f"- 💻 [GitHub]({github})")
        if cv:
            with open(cv, "rb") as f:
                st.download_button("📄 Descargar currículum", f, file_name=cv.split("/")[-1])

    st.markdown("### 👨‍💻 Equipo")

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        perfil("Pablo Iglesias Lareo",
               FOTO_PABLO,
               "https://www.linkedin.com/in/pablo-i-l",
               "https://github.com/Paulichenko0",
               CV_PABLO,
               ancho_foto=120)

    with col2:
        perfil("Carla Gámez Del Álamo",
               FOTO_CARLA,
               "https://www.linkedin.com/in/carlagamez/",
               "https://github.com/carlagamez",
               ancho_foto=140)

    with col3:
        perfil("Luis Bejerano Cobián",
               FOTO_LUIS,
               "https://www.linkedin.com/in/luis-bejerano-cobián-390172336",
               "https://github.com/LBEJECOBI",
               ancho_foto=145)

    with col4:
        perfil("Yones Smaha",
               FOTO_YONES,
               "https://www.linkedin.com/in/yones-smaha-nhaili-578372338",
               "https://github.com/senoy99",
               ancho_foto=205)

    st.markdown("---")
