import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np

def show_charts_page():
    """Vista de gráficos interactivos sobre alquiler de inmuebles."""
    
    # Título principal
    st.title("📈 Análisis de Alquileres en Madrid")

    # Ruta al archivo CSV
    csv_path = r"E:\Proyecto Final Bootcamp - copia\Proyecto Final\Pisos.com\Proyecto speed 1\Data Alquiler Unificado\alquiler_unificado_con_coordenadas_unicos.csv"

    # Verificar si el archivo existe
    if not os.path.exists(csv_path):
        st.error(f"⚠️ Archivo CSV no encontrado en la ruta: {csv_path}")
        return

    # Cargar los datos
    data = pd.read_csv(csv_path)

    # 1. Distribución de precios de alquiler
    if "precio_num" in data.columns:
        st.subheader("💰 Distribución de Precios de Alquiler")
        fig_precio = px.histogram(
            data, 
            x="precio_num", 
            nbins=50, 
            title="Distribución de Precios de Alquiler"
        )
        st.plotly_chart(fig_precio)
        
        # Texto de análisis debajo del gráfico
        st.markdown(
            """
            El gráfico muestra la distribución de frecuencias de los precios de alquiler representados en un histograma donde se observa que la mayoría de las propiedades se concentran en un rango de precios bajos con una cola que se extiende hacia valores más altos El eje vertical indica el porcentaje de propiedades que caen en cada intervalo mientras que el eje horizontal representa el precio en unidades monetarias La presencia de valores atípicos es evidente en la cola derecha donde un pequeño porcentaje de propiedades alcanza precios significativamente más altos que la mayoría La distribución no sigue un patrón simétrico sino que presenta un sesgo positivo típico en datos de precios donde la mayoría se agrupa en valores bajos y pocos casos alcanzan valores elevados Esta visualización resulta útil para identificar el comportamiento general del mercado de alquiler destacando la asimetría en la distribución de precios y la concentración de la oferta en segmentos económicos
            """
        )
    else:
        st.warning("⚠️ La columna 'precio_num' no existe en el archivo CSV.")

    # 2. Relación Habitaciones vs Precio con transformación logarítmica
    if {"habitaciones_num", "precio_num"}.issubset(data.columns):
        # Aplicar transformación logarítmica al precio
        data["log_precio"] = np.log(data["precio_num"])
        
        st.subheader("🏠 Relación Habitaciones vs Precio")
        fig_habitaciones = px.scatter(
            data, 
            x="habitaciones_num", 
            y="log_precio", 
            title="Habitaciones vs Precio", 
            trendline="ols"
        )
        st.plotly_chart(fig_habitaciones)
        
        # Explicación debajo del gráfico
        st.markdown(
            """
            El gráfico presenta una relación positiva entre el número de habitaciones y el precio de las propiedades, evidenciado por la tendencia ascendente de los puntos a medida que aumenta la cantidad de habitaciones Sin embargo, la dispersión de los datos indica que esta correlación no es perfecta y que otros factores influyen en el precio La escala logarítmica del eje Y sugiere que las diferencias en precios altos son menos pronunciadas visualmente, mientras que el rango amplio en el eje X revela una distribución heterogénea con propiedades desde 0 hasta alrededor de 300 habitaciones Llama la atención la presencia de valores atípicos particularmente en el extremo superior de habitaciones donde algunos casos muestran precios relativamente bajos en comparación con lo esperado Esta visualización resulta útil para identificar patrones generales pero requiere análisis complementarios para comprender mejor los factores subyacentes que afectan la variabilidad observada
            """
        )
    else:
        st.warning("⚠️ No se encontraron las columnas necesarias.")

    # 3. Ubicación de los inmuebles en alquiler con colores intensos
    if {"lat", "lon"}.issubset(data.columns):
        st.subheader("📍 Ubicación de los Inmuebles en Alquiler")
        
        # Filtrar precios entre 0 y 5000
        data = data[(data["precio_num"] >= 0) & (data["precio_num"] <= 5000)]
        
        fig_map = px.scatter_mapbox(
            data, 
            lat="lat", 
            lon="lon", 
            hover_name="titulo_y",
            color="precio_num", 
            title="Mapa de Alquileres",
            color_continuous_scale="Plasma",  # Colores fuertes y visibles
            zoom=12, 
            height=500
        )
        fig_map.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig_map)
    else:
        st.warning("⚠️ No se encontraron coordenadas.")