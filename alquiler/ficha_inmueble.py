import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from utils import cargar_datos

def show_ficha_inmueble():
    # --- Cargar datos ---
    @st.cache_data
    def cargar_filtrados():
        df = cargar_datos("alquiler.csv")
        return df.dropna(subset=["titulo", "lat", "lon"])

    df = cargar_filtrados()

    st.title("📄 Ficha Detallada del Inmueble")

    # Selector de inmueble (únicos por título)
    titulos = df["titulo"].drop_duplicates().tolist()
    titulo_seleccionado = st.selectbox("Selecciona un inmueble", options=titulos)

    # Filtrar la fila seleccionada
    inmueble = df[df["titulo"] == titulo_seleccionado].iloc[0]

    # Mostrar información detallada
    st.subheader(inmueble["titulo"])
    st.markdown(f"**Ubicación:** {inmueble.get('ubicacion', 'No disponible')}")
    st.markdown(f"**Precio:** {int(inmueble['precio'])} €")
    st.markdown(f"**Precio por m²:** {int(inmueble['precio_m2']) if pd.notna(inmueble['precio_m2']) else 'No disponible'} €")
    st.markdown(f"**Conservación:** {inmueble.get('conservacion', 'No disponible')}")
    st.markdown(f"**Habitaciones:** {int(inmueble['habitaciones']) if pd.notna(inmueble['habitaciones']) else 'No disponible'}")
    st.markdown(f"**Baños:** {int(inmueble['baños']) if pd.notna(inmueble['baños']) else 'No disponible'}")
    st.markdown(f"**Superficie construida:** {int(inmueble['superficie_construida']) if pd.notna(inmueble['superficie_construida']) else 'No disponible'} m²")
    st.markdown(f"[Ver publicación original]({inmueble['link']})")

    # Mapa con folium
    st.subheader("📍 Ubicación exacta")
    m = folium.Map(location=[inmueble["lat"], inmueble["lon"]], zoom_start=15)
    folium.Marker(
        location=[inmueble["lat"], inmueble["lon"]],
        popup=inmueble["titulo"]
    ).add_to(m)
    st_folium(m, width=700)

    # Si tienes columna descripción, aquí puedes usar:
    if "descripcion" in inmueble:
        st.subheader("📝 Descripción del inmueble")
        st.write(inmueble["descripcion"])
