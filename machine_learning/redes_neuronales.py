import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
import folium
from folium.plugins import MarkerCluster
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import LabelEncoder

from config import MODELO_TENSORFLOW, SCALER_TF_X, SCALER_TF_Y, VENTAS_CSV

def show_redes_neuronales():
    st.title("🧠 Predicción de Precios de Viviendas con Red Neuronal (TensorFlow)")
    st.markdown("Ingrese los datos de la vivienda para predecir el precio utilizando una red neuronal previamente entrenada.")

    st.markdown("""
    ### 🔥Incluyendo:
    ✅ Precio real de la vivienda después de la predicción.  
    ✅ Cálculo de la diferencia entre el precio real y el precio predicho.  
    ✅ Visualización de datos con gráficos interactivos para mejor análisis.  
    """)

    @st.cache_resource
    def load_model_and_scaler():
        model = tf.keras.models.load_model(MODELO_TENSORFLOW)
        scaler_X = joblib.load(SCALER_TF_X)
        scaler_y = joblib.load(SCALER_TF_Y)
        return model, scaler_X, scaler_y

    model, scaler_X, scaler_y = load_model_and_scaler()
    df = pd.read_csv(VENTAS_CSV)

    label_encoder = LabelEncoder()
    df["tipo_vivienda_encoded"] = label_encoder.fit_transform(df["tipo_vivienda"])

    features = ["habitaciones", "baños", "superficie_util", "tipo_vivienda_encoded"]
    X = df[features].values
    X_scaled = scaler_X.transform(X)
    y = df["precio"].values.reshape(-1, 1)
    y_scaled = scaler_y.transform(y)

    st.subheader("📊 Datos del CSV")
    st.dataframe(df)

    st.sidebar.header("🔍 Datos de la Vivienda")
    titulo = st.sidebar.selectbox("Título de la vivienda", df["titulo"].unique())
    ubicacion = st.sidebar.selectbox("Ubicación", df["ubicacion"].unique())
    habitaciones = st.sidebar.selectbox("Habitaciones", list(range(1, 11)))
    banos = st.sidebar.selectbox("Baños", list(range(1, 6)))
    superficie_util = st.sidebar.selectbox("Superficie útil (m²)", list(range(30, 301)))
    tipo_vivienda = st.sidebar.selectbox("Tipo de vivienda", label_encoder.classes_)
    tipo_vivienda_encoded = label_encoder.transform([tipo_vivienda])[0]

    precio_predicho_deseescalado = None
    precio_real = None
    diferencia_precio = None

    if st.sidebar.button("🔮 Predecir precio"):
        input_data = np.array([[habitaciones, banos, superficie_util, tipo_vivienda_encoded]])
        input_data_scaled = scaler_X.transform(input_data)

        precio_predicho_scaled = model.predict(input_data_scaled)
        precio_predicho_deseescalado = scaler_y.inverse_transform(precio_predicho_scaled.reshape(-1, 1))[0][0]

        precio_real = df.loc[
            (df["habitaciones"] == habitaciones) &
            (df["baños"] == banos) &
            (df["superficie_util"] == superficie_util) &
            (df["tipo_vivienda"] == tipo_vivienda),
            "precio"
        ].values

        precio_real = precio_real[0] if len(precio_real) > 0 else None
        diferencia_precio = abs(precio_real - precio_predicho_deseescalado) if precio_real is not None else None

        st.subheader(f"💰 Precio predicho: {precio_predicho_deseescalado:,.2f} €")
        if precio_real is not None:
            st.subheader(f"🏠 Precio real: {precio_real:,.2f} €")
            st.subheader(f"🔎 Diferencia entre precios: {diferencia_precio:,.2f} €")

    st.subheader("🗺️ Ubicación de las viviendas en el mapa")
    m = folium.Map(location=[df["lat"].mean(), df["lon"].mean()], zoom_start=12)
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in df.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=f"🏠 {row['titulo']}<br>💰 Precio: {row['precio']} €<br>📍 Ubicación: {row['ubicacion']}",
            tooltip=row["titulo"]
        ).add_to(marker_cluster)

    st.components.v1.html(m._repr_html_(), height=600)

    st.subheader("📈 Distribución de Precios de Viviendas")
    fig_dist = px.histogram(df, x="precio", nbins=30, title="Distribución de Precios de Viviendas", labels={"precio": "Precio (€)"})

    if precio_predicho_deseescalado is not None:
        try:
            y_max = max(fig_dist.data[0].y)
        except Exception:
            y_max = 50

        fig_dist.add_shape(
            type="line",
            x0=precio_predicho_deseescalado, x1=precio_predicho_deseescalado,
            y0=0, y1=y_max,
            line=dict(color="red", width=3, dash="dash"),
        )

        fig_dist.add_annotation(
            x=precio_predicho_deseescalado, y=y_max,
            text=f"💰 Precio Predicho: {precio_predicho_deseescalado:,.2f} €",
            showarrow=True,
            arrowhead=2,
            font=dict(color="red", size=12)
        )

    st.plotly_chart(fig_dist)

    st.subheader("📊 Comparación entre precios reales y predichos")
    y_real_flat = df["precio"].values.flatten()
    y_pred_scaled = model.predict(X_scaled)
    y_pred_flat = scaler_y.inverse_transform(y_pred_scaled).flatten()

    fig_real_vs_pred = go.Figure()
    fig_real_vs_pred.add_trace(go.Scatter(x=y_real_flat, y=y_pred_flat, mode="markers", marker=dict(size=8, opacity=0.6), name="Predicciones"))
    fig_real_vs_pred.add_trace(go.Scatter(x=[min(y_real_flat), max(y_real_flat)], y=[min(y_real_flat), max(y_real_flat)], mode="lines", line=dict(dash="dash", color="red"), name="Referencia"))
    st.plotly_chart(fig_real_vs_pred)

    st.subheader("📉 Evolución del Error Cuadrático Medio (MSE)")
    history = model.fit(X_scaled, y_scaled, epochs=100, batch_size=32, verbose=0)
    mse_values = history.history["loss"]

    fig_mse = go.Figure()
    fig_mse.add_trace(go.Scatter(x=list(range(1, len(mse_values) + 1)), y=mse_values, mode="lines+markers", name="MSE"))
    st.plotly_chart(fig_mse)
