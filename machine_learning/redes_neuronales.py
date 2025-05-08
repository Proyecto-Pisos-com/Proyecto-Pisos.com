import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
import folium
from folium.plugins import MarkerCluster
import plotly.express as px
from config import MODELO_TENSORFLOW, SCALER_TF_X, SCALER_TF_Y, VENTAS_CSV

def show_redes_neuronales():
    st.title("🧠 Predicción de Precios de Viviendas con Red Neuronal (TensorFlow)")
    st.markdown("Ingrese los datos de la vivienda para predecir el precio utilizando una red neuronal previamente entrenada.")

    @st.cache_resource
    def load_model_and_scaler():
        model = tf.keras.models.load_model(MODELO_TENSORFLOW)
        scaler_X = joblib.load(SCALER_TF_X)
        scaler_y = joblib.load(SCALER_TF_Y)
        return model, scaler_X, scaler_y

    model, scaler_X, scaler_y = load_model_and_scaler()

    df = pd.read_csv(VENTAS_CSV)

    st.subheader("📄 Vista previa de datos")
    st.dataframe(df)

    # Entrada usuario
    st.sidebar.header("📋 Datos de entrada para predicción")
    titulo = st.sidebar.text_input("Título de la vivienda", "")
    ubicacion = st.sidebar.text_input("Ubicación", "")
    habitaciones = st.sidebar.slider("Habitaciones", 1, 10, 3)
    banos = st.sidebar.slider("Baños", 1, 5, 2)
    superficie_util = st.sidebar.slider("Superficie útil (m²)", 30, 300, 100)
    piso = st.sidebar.slider("Piso", 1, 10, 1)

    input_data = np.array([[habitaciones, banos, superficie_util, piso]])
    input_data_scaled = scaler_X.transform(input_data)

    if st.sidebar.button("🔮 Predecir precio"):
        pred_scaled = model.predict(input_data_scaled)
        precio_predicho = scaler_y.inverse_transform(pred_scaled.reshape(-1, 1))
        st.success(f"💰 Precio predicho: {precio_predicho[0][0]:,.2f} €")

    # Mapa
    st.subheader("🗺️ Mapa de Ubicaciones de Viviendas")
    m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=12)
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in df.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=f"<b>{row['titulo']}</b><br>Precio: {row['precio']} €<br>Ubicación: {row['ubicacion']}",
            tooltip=row['titulo']
        ).add_to(marker_cluster)

    st.components.v1.html(m._repr_html_(), height=600)

    # Histograma
    st.subheader("📊 Distribución de Precios")
    fig = px.histogram(df, x="precio", nbins=30, title="Distribución de Precios de Viviendas", labels={"precio": "Precio (€)"})
    fig.update_layout(xaxis_title="Precio (€)", yaxis_title="Frecuencia")
    st.plotly_chart(fig)
