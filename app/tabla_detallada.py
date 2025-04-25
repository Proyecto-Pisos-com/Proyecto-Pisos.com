import streamlit as st
import pandas as pd
from utils import cargar_datos

def show_tabla_detallada_page():
    st.title("📋 Tabla Detallada de Inmuebles")

    # Detectar si es alquiler o ventas
    modo = st.session_state.get("modo", "alquiler")
    nombre_csv = "alquiler.csv" if modo == "alquiler" else "ventas.csv"

    df = cargar_datos(nombre_csv)

    if df.empty:
        st.error("⚠️ No se pudo cargar el archivo de datos.")
        return

    st.sidebar.header("🎛️ Filtros")

    # Convertir columnas necesarias a int
    if "habitaciones" in df.columns:
        df["habitaciones"] = df["habitaciones"].astype(int)
    if "baños" in df.columns:
        df["baños"] = df["baños"].astype(int)

    # Filtro por precio
    if "precio" in df.columns:
        min_precio = int(df["precio"].min())
        max_precio = int(df["precio"].max())
        precio = st.sidebar.slider("Precio (€)", min_precio, max_precio, (min_precio, max_precio))
    else:
        st.warning("La columna 'precio' no está disponible en el archivo.")
        return

    # Filtro por habitaciones
    habitaciones = st.sidebar.multiselect("Habitaciones", sorted(df["habitaciones"].unique()), default=sorted(df["habitaciones"].unique()))

    # Filtro por baños
    baños = st.sidebar.multiselect("Baños", sorted(df["baños"].unique()), default=sorted(df["baños"].unique()))

    # Filtro por superficie si existe
    if "metros" in df.columns:
        min_metros = int(df["metros"].min())
        max_metros = int(df["metros"].max())
        superficie = st.sidebar.slider("Superficie (m²)", min_metros, max_metros, (min_metros, max_metros))
    else:
        superficie = (0, 10000)  # Valor arbitrario por si no existe la columna

    # Aplicar filtros
    df_filtrado = df[
        (df["precio"].between(precio[0], precio[1])) &
        (df["habitaciones"].isin(habitaciones)) &
        (df["baños"].isin(baños)) &
        (df["metros"].between(superficie[0], superficie[1]))
    ]

    st.dataframe(df_filtrado.sort_values("precio"))
    st.markdown(f"Se muestran **{len(df_filtrado)}** inmuebles que coinciden con los filtros.")
