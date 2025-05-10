import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import pickle
import folium
from folium.plugins import MarkerCluster
import plotly.express as px

# Cargar el modelo y el scaler entrenados
@st.cache_resource  # Cambiado a @st.cache_resource
def load_model_and_scaler():
    model = tf.keras.models.load_model("modelo_mejorado.keras")
    with open("scaler_X.pkl", "rb") as f:
        scaler_X = pickle.load(f)
    with open("scaler_y.pkl", "rb") as f:
        scaler_y = pickle.load(f)
    return model, scaler_X, scaler_y

model, scaler_X, scaler_y = load_model_and_scaler()

# Cargar el dataset
df = pd.read_csv("ventas.csv")

# Mostrar datos iniciales
st.title("Predicción de Precios de Viviendas")
st.markdown("Ingrese los datos de la vivienda para predecir el precio")

# Mostrar todo el dataframe (no solo las primeras filas)
st.subheader("Datos del CSV")
st.dataframe(df)

# Formulario de entrada de datos
st.sidebar.header("Datos de la Vivienda")
titulo = st.sidebar.text_input("Título de la vivienda", "")
ubicacion = st.sidebar.text_input("Ubicación", "")
habitaciones = st.sidebar.slider("Habitaciones", min_value=1, max_value=10, value=3)
banos = st.sidebar.slider("Baños", min_value=1, max_value=5, value=2)
superficie_util = st.sidebar.slider("Superficie útil (m²)", min_value=30, max_value=300, value=100)
piso = st.sidebar.slider("Piso", min_value=1, max_value=10, value=1)

# Preparar los datos para la predicción
input_data = np.array([[habitaciones, banos, superficie_util, piso]])
input_data_scaled = scaler_X.transform(input_data)

# Predecir el precio de la vivienda
if st.sidebar.button("Predecir precio"):
    # Realizamos la predicción
    precio_predicho_scaled = model.predict(input_data_scaled)
    
    # Desescalar el precio
    precio_predicho_deseescalado = scaler_y.inverse_transform(precio_predicho_scaled.reshape(-1, 1))
    
    st.subheader(f"Precio predicho para la vivienda: {precio_predicho_deseescalado[0][0]:,.2f} €")

# Mostrar el mapa con las ubicaciones de las viviendas
st.subheader("Ubicación de las viviendas en el mapa")

# Crear un mapa base
m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=12)

# Agregar un marcador para cada vivienda
marker_cluster = MarkerCluster().add_to(m)

for idx, row in df.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=f"Vivienda: {row['titulo']}<br>Precio: {row['precio']} €<br>Ubicación: {row['ubicacion']}",
        tooltip=row['titulo']
    ).add_to(marker_cluster)

# Mostrar el mapa
st.subheader("Mapa de Ubicaciones")
st.components.v1.html(m._repr_html_(), height=600)

# Crear un gráfico de distribución de precios usando Plotly
st.subheader("Distribución de Precios")
fig = px.histogram(df, x="precio", nbins=30, title="Distribución de Precios de Viviendas", labels={"precio": "Precio (€)"})
fig.update_layout(xaxis_title="Precio (€)", yaxis_title="Frecuencia")
st.plotly_chart(fig)

# Ejecutar la app
if __name__ == "__main__":
    st.write("### Aplicación de Predicción de Precios de Viviendas")
    st.markdown("Esta app permite predecir el precio de una vivienda basándose en las características proporcionadas y mostrar las ubicaciones de las viviendas en un mapa interactivo.")
