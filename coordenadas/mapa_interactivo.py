import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from utils import cargar_datos

def show_mapa_interactivo():
    # --- Cargar datos ---
    @st.cache_data
    def cargar_filtrados():
        df = cargar_datos("alquiler.csv")
        return df.dropna(subset=["lat", "lon", "ubicacion", "titulo", "precio", "link"])

    df = cargar_filtrados()

    st.title("🗺️ Mapa Estilo Google de Inmuebles en Alquiler")

    # --- SIDEBAR: Filtros ---
    st.sidebar.header("🔍 Filtros de búsqueda")

    # Buscar por zona
    zonas = sorted(df["ubicacion"].dropna().unique().tolist())
    busqueda = st.sidebar.text_input("Buscar zona")
    zonas_filtradas = [z for z in zonas if busqueda.lower() in z.lower()]

    # Selección de zona
    zona_seleccionada = st.sidebar.selectbox("Selecciona una zona", options=zonas_filtradas if zonas_filtradas else [""])

    # Filtrar por zona
    df_filtrado = df[df["ubicacion"] == zona_seleccionada] if zona_seleccionada else df.head(0)

    # Filtro de precio con verificación
    if not df_filtrado.empty:
        min_precio = int(df_filtrado["precio"].min())
        max_precio = int(df_filtrado["precio"].max())

        if min_precio < max_precio:
            precio_range = st.sidebar.slider("Rango de precio (€)", min_value=min_precio, max_value=max_precio, value=(min_precio, max_precio))
            df_filtrado = df_filtrado[(df_filtrado["precio"] >= precio_range[0]) & (df_filtrado["precio"] <= precio_range[1])]
        else:
            st.sidebar.info("No hay suficientes valores distintos de precio para aplicar el filtro.")

    # --- MAPA ---
    if not df_filtrado.empty:
        m = folium.Map(location=[df_filtrado["lat"].mean(), df_filtrado["lon"].mean()], zoom_start=13)

        for _, row in df_filtrado.iterrows():
            popup = f"""
            <b>{row['titulo']}</b><br>
            {int(row['precio'])} €<br>
            {row['ubicacion']}<br>
            <a href="{row['link']}" target="_blank">Ver anuncio</a>
            """
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=folium.Popup(popup, max_width=300)
            ).add_to(m)

        st_folium(m, width=1000)
        st.markdown(f"Se muestran **{len(df_filtrado)}** inmuebles en **{zona_seleccionada}**.")
    else:
        st.info("No hay inmuebles disponibles con los filtros seleccionados.")
