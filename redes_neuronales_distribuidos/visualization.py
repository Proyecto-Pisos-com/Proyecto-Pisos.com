import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import MarkerCluster

def show_detailed_table(df):
    """
    Muestra una tabla detallada con información completa sobre las viviendas.
    """

    st.subheader("📋 Datos Detallados de Viviendas")
    selected_columns = ["titulo", "ubicacion", "precio", "habitaciones", "baños", "superficie_util", "tipo_vivienda"]
    st.dataframe(df[selected_columns])

def plot_map(df, vivienda_lat=None, vivienda_lon=None):
    """
    Mapa interactivo con información detallada y centrado en la vivienda predicha.
    """

    st.subheader("🗺️ Ubicación de las viviendas en el mapa")

    # Determinar posición inicial del mapa
    map_center = [df["lat"].mean(), df["lon"].mean()]
    if vivienda_lat and vivienda_lon:
        map_center = [vivienda_lat, vivienda_lon]

    # Crear mapa con Folium
    m = folium.Map(location=map_center, zoom_start=12)
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in df.iterrows():
        popup_text = (
            f"🏠 <b>{row['titulo']}</b><br>"
            f"💰 <b>Precio:</b> {row['precio']} €<br>"
            f"📏 <b>Superficie:</b> {row['superficie_util']} m²<br>"
            f"🛏️ <b>Habitaciones:</b> {row['habitaciones']}<br>"
            f"🚿 <b>Baños:</b> {row['baños']}<br>"
            f"🏡 <b>Tipo:</b> {row['tipo_vivienda']}<br>"
            f"📍 <b>Ubicación:</b> {row['ubicacion']}"
        )
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=popup_text,
            tooltip=row["titulo"]
        ).add_to(marker_cluster)

    st.components.v1.html(m._repr_html_(), height=600)

def plot_distribution(df, precio_predicho=None):
    """
    Distribución de precios con una línea roja en el precio predicho.
    """

    st.subheader("📈 Distribución de Precios")

    fig = px.histogram(df, x="precio", nbins=30, title="Distribución de Precios")

    if precio_predicho is not None:
        y_max = max(fig.data[0]["y"]) if fig.data and fig.data[0]["y"] is not None else 50  

        fig.add_shape(
            type="line",
            x0=precio_predicho, x1=precio_predicho,
            y0=0, y1=y_max,
            line=dict(color="red", width=3, dash="dash"),
        )

        fig.add_annotation(
            x=precio_predicho, y=y_max,
            text=f"💰 Precio Predicho: {precio_predicho:,.2f} €",
            showarrow=True,
            arrowhead=2,
            font=dict(color="red", size=12)
        )

    st.plotly_chart(fig)

def plot_price_comparison(df, model, scaler_X, scaler_y):
    """
    Gráfico de comparación entre precios reales y predichos.
    - Eje X: Precio real en euros.
    - Eje Y: Precio predicho en euros.
    - Línea roja fija que no cambia con la predicción.
    """

    st.subheader("📊 Comparación entre precios reales y predichos")
    
    y_real_flat = df["precio"].values.flatten()
    y_pred_scaled = model.predict(scaler_X.transform(df[["habitaciones", "baños", "superficie_util", "tipo_vivienda_encoded"]]))
    y_pred_flat = scaler_y.inverse_transform(y_pred_scaled).flatten()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=y_real_flat, y=y_pred_flat, mode="markers",
                             marker=dict(size=8, opacity=0.6), name="Predicciones"))
    
    # Línea roja fija que no cambia con la predicción
    min_val = min(y_real_flat.min(), y_pred_flat.min())
    max_val = max(y_real_flat.max(), y_pred_flat.max())
    
    fig.add_trace(go.Scatter(x=[min_val, max_val], y=[min_val, max_val], mode="lines",
                             line=dict(dash="dash", color="red"), name="Referencia (Real = Predicho)"))

    fig.update_layout(title="Comparación entre precios reales y predichos",
                      xaxis_title="Precio real (€)",
                      yaxis_title="Precio predicho (€)",
                      template="plotly_white",
                      showlegend=True)

    st.plotly_chart(fig)

def plot_mse(df, model, scaler_X, scaler_y):
    """
    Gráfico de evolución del error cuadrático medio (MSE) durante el entrenamiento.
    - Eje X: Épocas de entrenamiento (iteraciones)
    - Eje Y: Magnitud del error cuadrático medio (MSE), que mide la precisión del modelo.
    """

    st.subheader("📉 Evolución del Error Cuadrático Medio (MSE)")

    # Entrenar modelo para obtener el historial del MSE
    history = model.fit(scaler_X.transform(df[["habitaciones", "baños", "superficie_util", "tipo_vivienda_encoded"]]),
                        scaler_y.transform(df[["precio"]]), epochs=100, batch_size=32, verbose=0)
    
    mse_values = history.history["loss"]

    # Crear gráfico
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(1, len(mse_values) + 1)), y=mse_values,
                             mode="lines+markers", name="MSE"))

    fig.update_layout(title="Evolución del Error Cuadrático Medio (MSE)",
                      xaxis_title="Épocas (Iteraciones)",
                      yaxis_title="Magnitud del Error (MSE)",
                      template="plotly_white")

    st.plotly_chart(fig)
