import streamlit as st
from utils import cargar_datos

def show_detail_page():
    st.title("🔍 Detalle de inmuebles en alquiler")

    df = cargar_datos("alquiler.csv")

    if df.empty or "titulo" not in df.columns:
        st.error("⚠️ No se pudo cargar el archivo o falta la columna 'titulo'")
        return

    titulos = df["titulo"].dropna().unique().tolist()

    seleccionado = st.selectbox("Selecciona un inmueble:", titulos)

    inmueble = df[df["titulo"] == seleccionado]

    if inmueble.empty:
        st.warning("No se encontraron datos para el inmueble seleccionado.")
        return

    st.subheader("📋 Información del inmueble")
    st.dataframe(inmueble)

    # Si hay coordenadas, mostramos el mapa
    if {"lat", "lon"}.issubset(inmueble.columns):
        import folium
        from streamlit_folium import folium_static

        lat = inmueble.iloc[0]["lat"]
        lon = inmueble.iloc[0]["lon"]

        st.subheader("📍 Ubicación en el mapa")
        mapa = folium.Map(location=[lat, lon], zoom_start=15)
        folium.Marker(location=[lat, lon], popup=seleccionado).add_to(mapa)
        folium_static(mapa)
