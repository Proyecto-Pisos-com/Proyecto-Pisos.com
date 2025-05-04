# App_Pisos/app/deal_page.py

import joblib
from pathlib import Path

import pandas as pd
import streamlit as st

def show_deal_detector():
    st.title("🔍 Detector de ofertas (Chollo / Justo / Sobreprecio)")

    # ——— Rutas ———
    ROOT       = Path(__file__).resolve().parents[2]
    MODELS_DIR = ROOT / "models"
    DATA_CSV   = ROOT / "App_Pisos" / "app" / "data" / "alquiler.csv"

    # ——— Comprobar artefactos ———
    necesarios = {
        "KMeans":        MODELS_DIR / "kmeans_alquiler.pkl",
        "Scaler":        MODELS_DIR / "scaler_alquiler.pkl",
        "Regresión":     MODELS_DIR / "modelo_lgbm_alquiler.pkl",
        "Classifier":    MODELS_DIR / "clf_deal.pkl",
        "LabelEncoder":  MODELS_DIR / "le_deal.pkl",
    }
    faltantes = [nombre for nombre, p in necesarios.items() if not p.exists()]
    if faltantes:
        st.error("Faltan modelos en models/: " + ", ".join(faltantes))
        return

    # ——— Cargar artefactos ———
    km     = joblib.load(necesarios["KMeans"])
    scaler = joblib.load(necesarios["Scaler"])
    reg    = joblib.load(necesarios["Regresión"])
    clf    = joblib.load(necesarios["Classifier"])
    le     = joblib.load(necesarios["LabelEncoder"])

    # ——— Cargar CSV de alquileres ———
    df = pd.read_csv(DATA_CSV)
    df = df.dropna(subset=["precio","superficie_construida","lat","lon"])
    df["precio_m2"] = df.precio / df.superficie_construida
    df["cluster"]   = km.predict(df[["lat","lon"]])

    # ——— Entradas del usuario ———
    st.sidebar.header("Parámetros del inmueble")
    h   = st.sidebar.number_input("Habitaciones",           1, 0, 1)
    b   = st.sidebar.number_input("Baños",                  1, 0, 1)
    m   = st.sidebar.number_input("Superficie (m²)",      50.0, 0.0, 1.0)
    p   = st.sidebar.number_input("Precio (€)",           500.0, 0.0, 10.0)
    lat = st.sidebar.number_input("Latitud",         40.416775, format="%.6f")
    lon = st.sidebar.number_input("Longitud",       -3.703790, format="%.6f")

    if st.sidebar.button("Clasificar"):
        # — Feature engineering para este punto —
        precio_m2 = p / m if m else 0.0
        cluster_n = int(km.predict([[lat, lon]])[0])
        feats     = [[h, b, m, precio_m2, lat, lon, cluster_n]]
        Xs        = scaler.transform(feats)

        # — Predicción y etiqueta —
        label_code    = clf.predict(Xs)[0]
        label         = le.inverse_transform([label_code])[0]
        precio_pred   = reg.predict(Xs)[0]
        dev_rel       = (p - precio_pred) / precio_pred

        # — Mostrar resultado y explicación —
        st.markdown(f"## Resultado: **{label}**")
        st.markdown(f"- **Precio predicho:** €{precio_pred:,.0f}")
        st.markdown(f"- **Desviación:** {dev_rel*100:+.2f}% respecto al valor esperado")

        # — Contexto geográfico: muestra los 50 chollos más cercanos —
        df["dev_rel"] = (df["precio"] - reg.predict(scaler.transform(
            df[["habitaciones","baños","superficie_construida","precio_m2","lat","lon","cluster"]]
        ))) / reg.predict(scaler.transform(
            df[["habitaciones","baños","superficie_construida","precio_m2","lat","lon","cluster"]]
        ))
        # Filtrar solo “Chollos”
        chollos = df[df["dev_rel"] < -0.10].copy()
        # Calcular distancia aproximada (euclidiana) y ordenar
        chollos["dist"] = ((chollos.lat - lat)**2 + (chollos.lon - lon)**2)**0.5
        cercanos = chollos.nsmallest(50, "dist")

        st.markdown("### Mapa: 50 chollos más cercanos")
        st.map(cercanos[["lat","lon"]])

        st.markdown("### Tabla de chollos cercanos")
        st.dataframe(
            cercanos[["titulo","ubicacion","precio","precio_m2","dev_rel"]]
            .assign(dev_rel=lambda d: (d.dev_rel*100).round(2).astype(str) + "%")
            .rename(columns={"titulo":"Título","ubicacion":"Ubicación","precio":"Precio (€)","precio_m2":"€/m²","dev_rel":"Desviación"})
        )