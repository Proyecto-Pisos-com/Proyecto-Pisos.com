# App_Pisos/app/deal_page.py

import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import folium
from streamlit_folium import st_folium

@st.cache_data
def cargar_datos():
    csv_path = Path(__file__).resolve().parents[2] / "App_Pisos" / "app" / "data" / "alquiler.csv"
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=["precio", "habitaciones", "baños", "superficie_construida", "lat", "lon", "distrito"])
    df = df[df.precio.between(200, 10000)]
    df["precio_m2"] = df.precio / df.superficie_construida
    return df

@st.cache_resource
def cargar_modelos():
    models_path = Path(__file__).resolve().parents[2] / "models"
    scaler = joblib.load(models_path / "scaler_alquiler.pkl")
    clf    = joblib.load(models_path / "clf_deal.pkl")
    le     = joblib.load(models_path / "le_deal.pkl")
    kmeans = joblib.load(models_path / "kmeans_alquiler.pkl")
    reg    = joblib.load(models_path / "modelo_lgbm_alquiler.pkl")
    return scaler, clf, le, kmeans, reg

def show_deal_detector():
    """
    Página Streamlit para explorar ofertas:
    - Filtros por distrito, precio y superficie
    - Clasificación (Chollo/Justo/Sobreprecio)
    - Tabla HTML con enlaces
    - Mapa interactivo con folium
    - Explicación del método
    """
    st.title("🔎 Explorador de Ofertas de Alquiler")
    st.markdown("Filtra y visualiza inmuebles clasificados como chollo, justo o sobreprecio.")

    df = cargar_datos()
    scaler, clf, le, kmeans, reg = cargar_modelos()

    # — Filtros de usuario —
    distritos = ["Todos"] + sorted(df["distrito"].unique())
    distrito  = st.selectbox("📍 Selecciona distrito:", distritos)
    precio_max = st.slider("💰 Precio máximo (€):", 200, 5000, 1500, step=50)
    min_m2     = st.slider("📐 Superficie mínima (m²):", 20, 200, 50, step=5)

    df_filt = df.copy()
    if distrito != "Todos":
        df_filt = df_filt[df_filt.distrito == distrito]
    df_filt = df_filt[(df_filt.precio <= precio_max) & (df_filt.superficie_construida >= min_m2)]

    if df_filt.empty:
        st.warning("No hay propiedades que coincidan con los filtros seleccionados.")
        return

    # — Clasificación —
    df_filt["cluster"] = kmeans.predict(df_filt[["lat", "lon"]])
    feats        = df_filt[["habitaciones", "baños", "superficie_construida", "precio_m2", "lat", "lon", "cluster"]]
    feats_scaled = scaler.transform(feats)
    codes        = clf.predict(feats_scaled)
    labels       = le.inverse_transform(codes)
    df_filt["clasificación"] = labels

    # — Preparar tabla —
    def icono(et): 
        return "🟢 Chollo" if et == "Chollo" else ("🔴 Sobreprecio" if et == "Sobreprecio" else "⚪ Justo")

    df_tabla = df_filt[[
        "titulo","precio","superficie_construida","precio_m2","distrito","clasificación","url"
    ]].copy()
    df_tabla["clasificación"] = df_tabla["clasificación"].map(icono)
    df_tabla = df_tabla.sort_values("precio")
    df_tabla["inmueble"] = df_tabla["url"].apply(lambda u: f'<a href="{u}" target="_blank">ver</a>')
    df_tabla = df_tabla.rename(columns={
        "titulo":"Título",
        "precio":"Precio (€)",
        "superficie_construida":"Superficie (m²)",
        "precio_m2":"€/m²",
        "distrito":"Distrito",
        "clasificación":"Clasificación"
    })[["Título","Precio (€)","Superficie (m²)","€/m²","Distrito","Clasificación","inmueble"]]

    st.markdown("### 📋 Resultados clasificados")
    st.markdown(df_tabla.to_html(escape=False, index=False), unsafe_allow_html=True)

    # — Mapa interactivo —
    st.markdown("### 🗺️ Mapa interactivo de resultados")
    center = [df_filt.lat.mean(), df_filt.lon.mean()]
    m = folium.Map(location=center, zoom_start=13)

    # Mapeo de colores: las claves deben coincidir con los valores de df_filt["clasificación"]
    colores = {
        "Chollo": "green",
        "Justo": "blue",
        "Sobreprecio": "red"
    }

    for _, r in df_filt.iterrows():
        label = r["clasificación"]            # "Chollo", "Justo" o "Sobreprecio"
        color = colores.get(label, "gray")    # azul para "Justo"
        folium.Marker(
            location=[r.lat, r.lon],
            popup=(
                f"<b>{r.titulo}</b><br>"
                f"Precio: {r.precio} €<br>"
                f"{icono(label)}<br>"
                f"<a href='{r.url}' target='_blank'>ver inmueble</a>"
            ),
            icon=folium.Icon(color=color)
        ).add_to(m)

    st_folium(m, width="100%", height=600)

    # — Explicación final —
    st.markdown("---")
    st.markdown("""
    **ℹ️ Cómo funciona**  
    - El modelo predice un precio esperado y calcula la desviación.  
    - Clasifica en:
      - 🟢 Chollo: muy por debajo del precio estimado.  
      - ⚪ Justo: precio cercano al estimado.  
      - 🔴 Sobreprecio: por encima del estimado.  
    - El mapa es interactivo: haz zoom y arrástralo para explorar.
<<<<<<< HEAD
    """)
=======
    """)
>>>>>>> 98cce31 (Importar carpeta limpieza-train con historial local)
