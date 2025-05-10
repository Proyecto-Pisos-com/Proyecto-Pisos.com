import streamlit as st
import pandas as pd
import joblib
import folium
from streamlit_folium import st_folium
from config import (
    ALQUILER_CSV,
    SCALER_ALQUILER,
    CLF_DEAL,
    LE_DEAL,
    KMEANS_ALQUILER,
)

@st.cache_data
def cargar_datos():
    df = pd.read_csv(ALQUILER_CSV)
    df.dropna(subset=["precio", "habitaciones", "baños", "superficie_construida", "lat", "lon", "distrito"], inplace=True)
    df = df[df.precio.between(200, 10000)]
    df["precio_m2"] = df.precio / df.superficie_construida
    return df

@st.cache_resource
def cargar_modelos():
    scaler = joblib.load(SCALER_ALQUILER)
    clf = joblib.load(CLF_DEAL)
    le = joblib.load(LE_DEAL)
    kmeans = joblib.load(KMEANS_ALQUILER)
    return scaler, clf, le, kmeans


def icono(clasificacion):
    return {
        "Chollo": "🟢 Chollo",
        "Justo": "🔵 Justo",
        "Sobreprecio": "🔴 Sobreprecio"
    }.get(clasificacion, "🔵 Justo")


def show_deal_detector():
    st.title("🔎 Explorador de Ofertas de Alquiler")
    st.markdown("Filtra y visualiza inmuebles clasificados como chollo, justo o sobreprecio.")

    df = cargar_datos()
    scaler, clf, le, kmeans = cargar_modelos()

    distrito = st.selectbox("📍 Selecciona distrito:", ["Todos"] + sorted(df["distrito"].unique()))
    precio_max = st.slider("💰 Precio máximo (€):", 200, 5000, 1500, step=50)
    min_m2 = st.slider("📐 Superficie mínima (m²):", 20, 200, 50, step=5)

    df_filt = df[(df.precio <= precio_max) & (df.superficie_construida >= min_m2)]
    if distrito != "Todos":
        df_filt = df_filt[df_filt.distrito == distrito]

    if df_filt.empty:
        st.warning("No hay propiedades que coincidan con los filtros seleccionados.")
        return

    df_filt["cluster"] = kmeans.predict(df_filt[["lat", "lon"]])
    features = df_filt[["habitaciones", "baños", "superficie_construida", "precio_m2", "lat", "lon", "cluster"]]
    scaled_features = scaler.transform(features)
    df_filt["clasificación"] = le.inverse_transform(clf.predict(scaled_features))

    df_tabla = df_filt[[
        "titulo", "precio", "superficie_construida", "precio_m2", "distrito", "clasificación", "url"
    ]].copy()

    df_tabla["Clasificación"] = df_tabla["clasificación"].apply(icono)
    df_tabla.sort_values("precio", inplace=True)
    df_tabla["Inmueble"] = df_tabla["url"].apply(lambda u: f'<a href="{u}" target="_blank">ver</a>')
    df_tabla.rename(columns={
        "titulo": "Título",
        "precio": "Precio (€)",
        "superficie_construida": "Superficie (m²)",
        "precio_m2": "€/m²",
        "distrito": "Distrito"
    }, inplace=True)

    df_tabla = df_tabla[["Título", "Precio (€)", "Superficie (m²)", "€/m²", "Distrito", "Clasificación", "Inmueble"]]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📋 Resultados clasificados")
        st.markdown(df_tabla.to_html(escape=False, index=False), unsafe_allow_html=True)

    with col2:
        st.markdown("### 🗺️ Localiza tu chollo")
        mapa = folium.Map(
            location=[df_filt.lat.mean(), df_filt.lon.mean()],
            zoom_start=13,
            tiles="CartoDB positron"
        )

        for _, row in df_filt.iterrows():
            folium.Marker(
                location=[row.lat, row.lon],
                popup=(
                    f"<b>{row.titulo}</b><br>"
                    f"Precio: {row.precio} €<br>"
                    f"{icono(row['clasificación'])}<br>"
                    f"<a href='{row.url}' target='_blank'>ver inmueble</a>"
                ),
                icon=folium.Icon(color={"Chollo": "green", "Justo": "blue", "Sobreprecio": "red"}.get(row["clasificación"], "gray"))
            ).add_to(mapa)

        st_folium(mapa, use_container_width=True, height=500)

    st.markdown("""
    ---
    **ℹ️ Cómo funciona**  
    - El modelo predice un precio esperado y calcula la desviación.  
    - Clasifica en:
        - 🟢 Chollo: muy por debajo del precio estimado.  
        - 🔵 Justo: precio cercano al estimado.  
        - 🔴 Sobreprecio: por encima del estimado.
    """)