import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from utils import cargar_datos

def show_comparador_pisos():
    # --- Cargar datos ---
    @st.cache_data
    def cargar_filtrados():
        return cargar_datos("ventas.csv")

    df = cargar_filtrados()

    # --- Selección de inmuebles ---
    titulos = df['titulo'].drop_duplicates().tolist()
    titulo_1 = st.selectbox("Selecciona el primer inmueble", options=titulos, key="inm1_venta")
    titulo_2 = st.selectbox("Selecciona el segundo inmueble", options=[t for t in titulos if t != titulo_1], key="inm2_venta")

    # --- Filtrar inmuebles seleccionados ---
    df_comp = df[df['titulo'].isin([titulo_1, titulo_2])].copy()

    # --- Detectar tipo ---
    tipos = ['piso', 'casa', 'atico', 'estudio', 'apartamento', 'duplex', 'chalet', 'finca', 'loft']
    def detectar_tipo(row):
        for tipo in tipos:
            if tipo in row and row[tipo] == 1:
                return tipo.capitalize()
        return "Desconocido"
    
    df_comp['Inmueble'] = df_comp.apply(detectar_tipo, axis=1)

    # --- Mostrar enlaces ---
    st.markdown("### 🔗 Enlaces a los inmuebles seleccionados:")
    for _, row in df_comp.iterrows():
        st.markdown(f"[{row['titulo']}]({row['link']})")

    # --- Mostrar características clave ---
    columnas = ['Inmueble', 'precio', 'precio_m2', 'habitaciones', 'baños', 'superficie_construida']
    st.markdown("### 📋 Características del inmueble:")
    st.dataframe(df_comp[columnas], use_container_width=True)

    # --- Variables para gráficos ---
    vars_grande = ['precio', 'precio_m2', 'superficie_construida']
    vars_chico = ['habitaciones', 'baños']

    valores1_g = df_comp[df_comp['titulo'] == titulo_1][vars_grande].iloc[0]
    valores2_g = df_comp[df_comp['titulo'] == titulo_2][vars_grande].iloc[0]

    valores1_c = df_comp[df_comp['titulo'] == titulo_1][vars_chico].iloc[0]
    valores2_c = df_comp[df_comp['titulo'] == titulo_2][vars_chico].iloc[0]

    # --- Gráfico: Precio, €/m² y Superficie ---
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=vars_grande,
        y=valores1_g,
        name=titulo_1,
        text=valores1_g.values,
        textposition="outside",
        marker_color="blue",
        width=0.3,
        opacity=0.85,
        marker_line_width=1
    ))
    fig1.add_trace(go.Bar(
        x=vars_grande,
        y=valores2_g,
        name=titulo_2,
        text=valores2_g.values,
        textposition="outside",
        marker_color="red",
        width=0.3,
        opacity=0.85,
        marker_line_width=1
    ))
    fig1.update_layout(
        barmode='group',
        title="Comparación: Precio, €/m² y Superficie",
        yaxis_title="Valor",
        legend_title="Inmueble"
    )

    # --- Gráfico: Habitaciones y Baños ---
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=vars_chico,
        y=valores1_c,
        name=titulo_1,
        text=valores1_c.values,
        textposition="outside",
        marker_color="blue",
        width=0.3,
        opacity=0.85,
        marker_line_width=1
    ))
    fig2.add_trace(go.Bar(
        x=vars_chico,
        y=valores2_c,
        name=titulo_2,
        text=valores2_c.values,
        textposition="outside",
        marker_color="red",
        width=0.3,
        opacity=0.85,
        marker_line_width=1
    ))
    fig2.update_layout(
        barmode='group',
        title="Comparación: Habitaciones y Baños",
        yaxis_title="Cantidad",
        legend_title="Inmueble"
    )

    # --- Mostrar gráficos ---
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)
