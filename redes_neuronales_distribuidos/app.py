import streamlit as st
import pandas as pd
import data_loader
import model_loader
import ui_components
import visualization

# --- Definición de la aplicación ---
st.title("🏡 Aplicación de Predicción de Precios de Viviendas")
st.markdown("""
### 🔍 Podrás Visualizar:
✅ **Precio real** de la vivienda después de la predicción.  
✅ **Cálculo de la diferencia** entre el precio real y el precio predicho *(siempre que filtres los datos exactos de la vivienda detallada).*  
✅ **Indicación del precio predicho** en la gráfica de distribución de precios.  
✅ **Visualización de datos** con gráficos interactivos para mejor análisis.  
✅ **Mapa centrado automáticamente** en la vivienda predicha.  
""")

# --- Cargar datos y modelo ---
df = data_loader.load_data()
model, scaler_X, scaler_y = model_loader.load_model_and_scaler()

# --- Tabla detallada con información de todas las viviendas ---
visualization.show_detailed_table(df)

# --- Mostrar filtros y obtener datos de la vivienda predicha ---
precio_predicho, precio_real, diferencia_precio, vivienda_lat, vivienda_lon = ui_components.show_filters(df, model, scaler_X, scaler_y)

# --- Generar visualizaciones con el precio predicho ---
visualization.plot_map(df, vivienda_lat, vivienda_lon)
visualization.plot_distribution(df, precio_predicho)
visualization.plot_price_comparison(df, model, scaler_X, scaler_y)
visualization.plot_mse(df, model, scaler_X, scaler_y)
