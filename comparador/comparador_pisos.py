import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from utils import cargar_datos
from config import VENTAS_CSV
import plotly.graph_objects as go

def show_comparador_pisos():
    @st.cache_data
    def cargar_filtrados():
        return cargar_datos(VENTAS_CSV)

    df = cargar_filtrados()
    titulos = df['titulo'].drop_duplicates().tolist()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🏷️ Primer inmueble")
        titulo_1 = st.selectbox("", options=titulos, key="inm1_venta", label_visibility="collapsed")
    with col2:
        st.markdown("### 🏷️ Segundo inmueble")
        titulo_2 = st.selectbox("", options=[t for t in titulos if t != titulo_1], key="inm2_venta", label_visibility="collapsed")

    df_comp = df[df['titulo'].isin([titulo_1, titulo_2])].copy()
    piso_1 = df_comp[df_comp['titulo'] == titulo_1].iloc[0]
    piso_2 = df_comp[df_comp['titulo'] == titulo_2].iloc[0]

    st.markdown("### 🧾 Comparativa visual de inmuebles")
    c1, c2 = st.columns(2)

    def mostrar_ficha(piso, titulo):
        st.markdown(f"#### 🏡 {titulo}")
        st.markdown(f"**Tipo:** {piso.get('tipo_vivienda', 'N/A')}")
        st.markdown(f"**Precio:** {int(piso['precio']):,} €")
        st.markdown(f"**€/m²:** {int(piso['precio_m2']) if pd.notna(piso['precio_m2']) else 'N/A'} €")
        st.markdown(f"**Superficie construida:** {int(piso['superficie_construida'])} m²")
        st.markdown(f"**Habitaciones:** {int(piso['habitaciones'])}")
        st.markdown(f"**Baños:** {int(piso['baños'])}")
        st.markdown(f"[🔗 Ver publicación]({piso['link']})")

    with c1:
        mostrar_ficha(piso_1, titulo_1)
    with c2:
        mostrar_ficha(piso_2, titulo_2)

    vars_grande = ['precio', 'precio_m2', 'superficie_construida']
    vars_chico = ['habitaciones', 'baños']

    # Aplicar pesos visuales para mejorar visibilidad
    pesos_visuales_grande = {'precio': 1, 'precio_m2': 100, 'superficie_construida': 3000}
    fig1 = go.Figure()
    for var in vars_grande:
        v1 = piso_1[var] * pesos_visuales_grande.get(var, 1)
        v2 = piso_2[var] * pesos_visuales_grande.get(var, 1)
        fig1.add_trace(go.Bar(x=[var], y=[v1], name=titulo_1, marker_color="blue", text=[piso_1[var]], textposition="outside"))
        fig1.add_trace(go.Bar(x=[var], y=[v2], name=titulo_2, marker_color="orange", text=[piso_2[var]], textposition="outside"))
    fig1.update_layout(barmode='group', title="📊 Comparación económica", yaxis_title="Valor ajustado")

    fig2 = go.Figure()
    for var in vars_chico:
        fig2.add_trace(go.Bar(x=[var], y=[piso_1[var]], name=titulo_1, marker_color="blue", text=[piso_1[var]], textposition="outside"))
        fig2.add_trace(go.Bar(x=[var], y=[piso_2[var]], name=titulo_2, marker_color="orange", text=[piso_2[var]], textposition="outside"))
    fig2.update_layout(barmode='group', title="📐 Habitaciones y baños", yaxis_title="Cantidad")

    colg1, colg2 = st.columns(2)
    with colg1:
        st.plotly_chart(fig1, use_container_width=True)
    with colg2:
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 🥇 Comparativa visual total (valores ajustados)")

    categorias = ['Precio', '€/m²', 'Superficie', 'Habitaciones', 'Baños']
    valores_1 = [piso_1['precio'], piso_1['precio_m2'], piso_1['superficie_construida'],
                 piso_1['habitaciones'], piso_1['baños']]
    valores_2 = [piso_2['precio'], piso_2['precio_m2'], piso_2['superficie_construida'],
                 piso_2['habitaciones'], piso_2['baños']]

    pesos_visuales = {
        'Precio': 1,
        '€/m²': 200,
        'Superficie': 4000,
        'Habitaciones': 100000,
        'Baños': 100000
    }

    valores_1_ajustados = [v * pesos_visuales[c] for v, c in zip(valores_1, categorias)]
    valores_2_ajustados = [v * pesos_visuales[c] for v, c in zip(valores_2, categorias)]

    fig, ax = plt.subplots(figsize=(8, 5))
    y_pos = np.arange(len(categorias))
    ax.barh(y_pos, valores_1_ajustados, color='blue', label=titulo_1)
    ax.barh(y_pos, valores_2_ajustados, left=valores_1_ajustados, color='orange', label=titulo_2)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(categorias)
    ax.invert_yaxis()
    ax.set_xlabel("Valor (ajustado para visualización)")
    ax.set_title("Comparación por categoría (valores ajustados visualmente)")
    ax.legend()

    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    col3, col4 = st.columns([2, 1])
    with col3:
        st.image(buf)
    with col4:
        st.markdown("### 📌 Resumen de diferencias")
        for cat, v1, v2 in zip(categorias, valores_1, valores_2):
            if v1 > v2:
                st.markdown(f"✅ **{cat}:** Gana **{titulo_1}** con diferencia de **{v1 - v2:.1f}**")
            elif v2 > v1:
                st.markdown(f"✅ **{cat}:** Gana **{titulo_2}** con diferencia de **{v2 - v1:.1f}**")
            else:
                st.markdown(f"🔸 **{cat}:** Empate en ambos inmuebles.")
