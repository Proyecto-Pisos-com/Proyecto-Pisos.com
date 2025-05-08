import streamlit as st
import pandas as pd
import plotly.express as px
import folium
import json
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from utils import cargar_datos
from config import VENTAS_CSV, GEOJSON_DISTRITOS

def show_charts_page():
    st.title("📈 Análisis de Ventas de Inmuebles en Madrid")

    df = cargar_datos(VENTAS_CSV)

    if df.empty:
        st.error("⚠️ No se pudo cargar el archivo de ventas.")
        return

    # --- Limpieza de distritos y tipo de vivienda ---
    df["distrito"] = df["distrito"].str.strip().str.title()
    df["distrito"] = df["distrito"].replace({
        "Barrio De Salamanca": "Salamanca",
        "Puente De Vallecas": "Puente de Vallecas",
        "Villa De Vallecas": "Villa de Vallecas"
    })

    tipo_columnas = {
        "piso": "Piso", "casa": "Casa", "ático": "Ático", "estudio": "Estudio",
        "apartamento": "Apartamento", "duplex": "Dúplex", "chalet": "Chalet",
        "finca": "Finca", "loft": "Loft"
    }

    def detectar_tipo(row):
        for col, nombre in tipo_columnas.items():
            if col in row and row[col] == 1:
                return nombre
        return "Otro"

    df["tipo_vivienda"] = df.apply(detectar_tipo, axis=1)

    if "precio_m2" not in df.columns and "superficie_construida" in df.columns:
        df["precio_m2"] = df["precio"] / df["superficie_construida"]

    # --- HISTOGRAMA ---
    st.subheader("💰 Distribución de Precios de Venta")
    fig_hist = px.histogram(
        df, x="precio", nbins=50,
        title="Distribución de Precios de Venta",
        color_discrete_sequence=["#636EFA"]
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    # --- MAPAS EN DOS COLUMNAS ---
    st.subheader("🗺️ Comparativa de Mapas")

    col1, col2 = st.columns(2)

    # --- MAPA COROPLÉTICO ---
    with col1:
        st.markdown("#### 📍 Mapa Coroplético por Distrito")
        variable = st.selectbox(
            "Variable a visualizar:",
            options=["precio", "precio_m2", "superficie_construida", "habitaciones"],
            format_func=lambda x: {
                "precio": "Precio Medio (€)",
                "precio_m2": "Precio por m² (€)",
                "superficie_construida": "Superficie Media (m²)",
                "habitaciones": "Habitaciones Medias"
            }[x],
            key="var_coropletico"
        )

        media = df.groupby("distrito")[variable].mean().reset_index()
        media.columns = ["distrito", "valor"]

        with open(GEOJSON_DISTRITOS, encoding="utf-8") as f:
            geojson = json.load(f)

        mapa_coro = folium.Map(location=[40.4168, -3.7038], zoom_start=11, tiles="CartoDB positron")

        choropleth = folium.Choropleth(
            geo_data=geojson,
            name="choropleth",
            data=media,
            columns=["distrito", "valor"],
            key_on="feature.properties.name",
            fill_color="YlOrRd",
            fill_opacity=0.7,
            line_opacity=0.2,
            nan_fill_color="gray",
            legend_name=f"{variable.replace('_', ' ').capitalize()} por distrito"
        ).add_to(mapa_coro)

        folium.GeoJsonTooltip(
            fields=["name"],
            aliases=["Distrito:"],
            labels=True,
            sticky=True,
            style=("background-color: white; font-size: 13px; padding: 5px;")
        ).add_to(choropleth.geojson)

        folium.LayerControl().add_to(mapa_coro)
        folium_static(mapa_coro, width=800, height=500)

    # --- MAPA INTERACTIVO ---
    with col2:
        st.markdown("#### 🏘️ Mapa de Inmuebles")

        distritos_disponibles = ["Todos"] + sorted(df["distrito"].dropna().unique())
        distrito_sel = st.selectbox("Filtrar por distrito", distritos_disponibles, key="filtro_distrito")

        df_filtrado = df if distrito_sel == "Todos" else df[df["distrito"] == distrito_sel]

        mapa_pts = folium.Map(location=[40.4168, -3.7038], zoom_start=12, tiles="CartoDB positron")
        marker_cluster = MarkerCluster().add_to(mapa_pts)

        for _, row in df_filtrado.iterrows():
            if pd.notna(row["lat"]) and pd.notna(row["lon"]):
                popup = (
                    f"<strong>{row['distrito']}</strong><br>"
                    f"💰 Precio: {row['precio']:.0f} €<br>"
                    f"📏 Superficie: {row['superficie_construida']} m²<br>"
                    f"🛏 Habitaciones: {row['habitaciones']}<br>"
                    f"🛁 Baños: {row['baños']}<br>"
                    f"🏘 Tipo: {row['tipo_vivienda']}"
                )
                folium.Marker(
                    location=[row["lat"], row["lon"]],
                    popup=popup,
                    icon=folium.Icon(color="blue", icon="home")
                ).add_to(marker_cluster)

        folium_static(mapa_pts, width=800, height=500)

    st.markdown("""
    Esta página muestra un análisis completo de los precios de venta en Madrid.  
    Puedes visualizar los datos de forma geográfica:

    - **Mapa coroplético:** compara diferentes métricas por distrito.
    - **Mapa de inmuebles:** explora propiedades individuales filtrables por distrito.
    """)