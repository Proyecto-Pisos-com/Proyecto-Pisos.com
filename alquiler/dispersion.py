import streamlit as st
import pandas as pd
import plotly.express as px
from utils import cargar_datos

def show_dispersion():

    # --- Cargar datos y detectar tipo de vivienda ---
    @st.cache_data
    def cargar_y_procesar_datos():
        df = cargar_datos("alquiler.csv")

        tipo_cols = [
            ("piso", "Piso"),
            ("casa", "Casa"),
            ("atico", "Ático"),
            ("estudio", "Estudio"),
            ("apartamento", "Apartamento"),
            ("duplex", "Dúplex"),
            ("chalet", "Chalet"),
            ("finca", "Finca"),
            ("loft", "Loft"),
        ]

        def detectar_tipo(row):
            for col, nombre in tipo_cols:
                if col in row and row[col] == 1:
                    return nombre
            return "Otro"

        df["tipo_vivienda"] = df.apply(detectar_tipo, axis=1)
        return df

    df = cargar_y_procesar_datos()

    # --- Título de la app ---
    st.title("🏘️ Análisis Interactivo de Inmuebles en Alquiler")

    # --- FILTROS EN SIDEBAR ---
    st.sidebar.header("🔎 Filtros")

    # Tipo de vivienda
    tipos_disponibles = sorted(df["tipo_vivienda"].dropna().unique())
    tipo_sel = st.sidebar.selectbox("Tipo de vivienda", ["Todos"] + tipos_disponibles)
    if tipo_sel != "Todos":
        df = df[df["tipo_vivienda"] == tipo_sel]

    # Zona / Barrio
    if "ubicacion" in df.columns:
        zonas = sorted(df["ubicacion"].dropna().unique())
        zona_sel = st.sidebar.selectbox("Zona / Barrio", ["Todos"] + zonas)
        if zona_sel != "Todos":
            df = df[df["ubicacion"] == zona_sel]

    # Rango de precios
    if "precio" in df.columns:
        min_precio = int(df["precio"].min())
        max_precio = int(df["precio"].max())
        precio_range = st.sidebar.slider("Rango de precios (€)", min_precio, max_precio, (min_precio, max_precio))
        df = df[(df["precio"] >= precio_range[0]) & (df["precio"] <= precio_range[1])]

    # Filtro por habitaciones
    if "habitaciones" in df.columns:
        min_hab = int(df["habitaciones"].min())
        max_hab = int(df["habitaciones"].max())
        hab_sel = st.sidebar.slider("Nº mínimo de habitaciones", min_hab, max_hab, min_hab)
        df = df[df["habitaciones"] >= hab_sel]

    # Filtro por baños
    if "baños" in df.columns:
        baños_unicos = sorted(df["baños"].dropna().unique())
        baños_sel = st.sidebar.multiselect("Nº de baños", baños_unicos, default=baños_unicos)
        df = df[df["baños"].isin(baños_sel)]

    # Filtro libre
    st.sidebar.markdown("#### 🔍 Filtro libre por columna")
    columnas_opcionales = [c for c in df.columns if df[c].nunique() < 50 and c not in ["tipo_vivienda", "ubicacion", "baños", "habitaciones"]]
    if columnas_opcionales:
        col_filtro = st.sidebar.selectbox("Selecciona una columna", columnas_opcionales)
        opciones_col = sorted(df[col_filtro].dropna().unique().tolist())
        sel_valores = st.sidebar.multiselect(f"Valores de '{col_filtro}'", opciones_col, default=opciones_col)
        df = df[df[col_filtro].isin(sel_valores)]

    # --- GRÁFICO DISPERSIÓN ---
    st.subheader("💡 Relación Precio vs Superficie")

    color_map = {
        "Ático": "black",
        "Apartamento": "darkgreen"
    }

    fig = px.scatter(
        df,
        x="superficie_construida",
        y="precio",
        color="tipo_vivienda",
        color_discrete_map=color_map,
        hover_data=["titulo", "ubicacion", "habitaciones", "baños"],
        labels={
            "superficie_construida": "Superficie Construida (m²)",
            "precio": "Precio (€)"
        },
        title="Relación entre Precio y Superficie Construida"
    )
    st.plotly_chart(fig)

    # --- TABLA RESUMEN ---
    st.subheader("📋 Resumen Estadístico")

    columnas_resumen = ["precio", "superficie_construida"]
    df_resumen = df.groupby("tipo_vivienda")[columnas_resumen].agg(["mean", "min", "max", "std"]).round(2)
    df_resumen.columns = ['_'.join(col) for col in df_resumen.columns]
    df_resumen = df_resumen.reset_index(drop=True)

    df_resumen = df_resumen.rename(columns={
        'precio_mean': 'alquiler_mensual_media',
        'precio_min': 'alquiler_mensual_min',
        'precio_max': 'alquiler_mensual_max',
        'precio_std': 'alquiler_mensual_desviacion_estandar',
        'superficie_construida_mean': 'superficie_construida_media'
    })

    st.dataframe(df_resumen[[ 
        "alquiler_mensual_media", "alquiler_mensual_min", "alquiler_mensual_max",
        "alquiler_mensual_desviacion_estandar", "superficie_construida_media"
    ]], use_container_width=True)

    # --- TEXTO RESUMEN AUTOMÁTICO ---
    if not df_resumen.empty:
        media = df_resumen["alquiler_mensual_media"].iloc[0]
        desv = df_resumen["alquiler_mensual_desviacion_estandar"].iloc[0]

        if pd.notnull(media) and pd.notnull(desv):
            rango_min = int(media - desv)
            rango_max = int(media + desv)
            st.markdown(f"""
            📌 La **media de alquiler mensual** es de **{media:.0f} €** con una **desviación estándar de {desv:.0f} €**.
            Esto significa que la mayoría de los precios se encuentran entre **{rango_min} € y {rango_max} €**.
            """)
        else:
            st.info("No hay suficientes datos para calcular la media o la desviación estándar.")

    # --- DESCRIPCIÓN FINAL ---
    st.markdown("""
    Este panel te permite:
    - Combinar múltiples filtros como tipo, zona, habitaciones, baños y criterios personalizados
    - Visualizar la relación entre precio y superficie
    - Consultar estadísticas útiles para decisiones informadas
    """)
