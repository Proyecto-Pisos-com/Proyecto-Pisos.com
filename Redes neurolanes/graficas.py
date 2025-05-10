import plotly.express as px
import numpy as np
import streamlit as st

def mostrar_grafico(y_test, predicciones):
    """Muestra una gráfica interactiva con escala logarítmica."""
    y_test_log = np.log1p(y_test)
    predicciones_log = np.log1p(predicciones)

    fig = px.scatter(
        x=y_test_log, 
        y=predicciones_log,
        labels={"x": "Log(Precio real)", "y": "Log(Precio predicho)"},
        title="📊 Predicciones vs Valores Reales",
        opacity=0.7
    )

    fig.add_shape(
        type="line",
        x0=y_test_log.min(),
        x1=y_test_log.max(),
        y0=y_test_log.min(),
        y1=y_test_log.max(),
        line=dict(color="red", dash="dash")
    )

    st.plotly_chart(fig)
