import streamlit as st
import sqlite3
import pandas as pd
import os
from config import (
    DATABASE_ALQUILER, DATABASE_VENTAS,
    DATA_BASE_ALQUILER, DATA_BASE_VENTAS
)

# --- Ejecutar consulta SQL ---
def ejecutar_sql(ruta_bd, query):
    conn = sqlite3.connect(ruta_bd)
    try:
        resultado = pd.read_sql_query(query, conn)
        return resultado
    except Exception as e:
        st.error(f"❌ Error en la consulta: {e}")
        return None
    finally:
        conn.close()

# --- Obtener listado de tablas (opcional) ---
def obtener_tablas(ruta_bd):
    conn = sqlite3.connect(ruta_bd)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = [fila[0] for fila in cursor.fetchall()]
    conn.close()
    return tablas

# --- Mostrar imagen ilustrativa de la base ---
def mostrar_imagen_bd(tipo):
    if tipo == "Alquiler":
        ruta_imagen = DATA_BASE_ALQUILER
    else:
        ruta_imagen = DATA_BASE_VENTAS

    if os.path.exists(ruta_imagen):
        st.image(ruta_imagen, use_container_width=True)

# --- Mostrar explorador SQL ---
def show_sql_explorer():
    st.markdown("## 🗂️ Explorador de Bases de Datos Inmobiliarias")

    # --- Seleccionar base de datos ---
    tipo = st.radio("Selecciona una base de datos:", ["Alquiler", "Ventas"], horizontal=True)
    ruta_bd = DATABASE_ALQUILER if tipo == "Alquiler" else DATABASE_VENTAS

    st.markdown("### 🔎 Consultas rápidas:")
    consulta_rapida = st.selectbox(
        "📌 Elige una consulta predefinida:",
        [
            "",
            "Anuncios con precio mayor a 3000€",
            "Pisos con más de 3 habitaciones",
            "Viviendas tipo ático",
            "Pisos con 2 baños y 3 habitaciones",
            "Top 10 por mayor precio/m²",
            "Top 5 pisos con más baños",
            "Piso con mayor superficie construida y su precio",
            "Piso con menor superficie construida y su precio",
            "Piso más caro",
            "Piso más barato"
        ]
    )

    consulta_por_defecto = ""
    if consulta_rapida == "Anuncios con precio mayor a 3000€":
        consulta_por_defecto = "SELECT * FROM anuncios WHERE precio > 3000;"
    elif consulta_rapida == "Pisos con más de 3 habitaciones":
        consulta_por_defecto = "SELECT * FROM anuncios WHERE habitaciones > 3;"
    elif consulta_rapida == "Viviendas tipo ático":
        consulta_por_defecto = "SELECT * FROM anuncios WHERE tipo_vivienda = 'atico';"
    elif consulta_rapida == "Pisos con 2 baños y 3 habitaciones":
        consulta_por_defecto = "SELECT * FROM anuncios WHERE baños = 2 AND habitaciones = 3;"
    elif consulta_rapida == "Top 10 por mayor precio/m²":
        consulta_por_defecto = "SELECT * FROM anuncios ORDER BY precio_m2 DESC LIMIT 10;"
    elif consulta_rapida == "Top 5 pisos con más baños":
        consulta_por_defecto = "SELECT * FROM anuncios ORDER BY baños DESC LIMIT 5;"
    elif consulta_rapida == "Piso con mayor superficie construida y su precio":
        consulta_por_defecto = "SELECT titulo, superficie_construida, precio FROM anuncios ORDER BY superficie_construida DESC LIMIT 1;"
    elif consulta_rapida == "Piso con menor superficie construida y su precio":
        consulta_por_defecto = "SELECT titulo, superficie_construida, precio FROM anuncios WHERE superficie_construida IS NOT NULL ORDER BY superficie_construida ASC LIMIT 1;"
    elif consulta_rapida == "Piso más caro":
        consulta_por_defecto = "SELECT titulo, precio, ubicacion FROM anuncios ORDER BY precio DESC LIMIT 1;"
    elif consulta_rapida == "Piso más barato":
        consulta_por_defecto = "SELECT titulo, precio, ubicacion FROM anuncios WHERE precio > 0 ORDER BY precio ASC LIMIT 1;"

    if consulta_por_defecto:
        if st.button("📥 Cargar consulta"):
            st.session_state["consulta_sql"] = consulta_por_defecto

    # --- Entrada para consulta SQL ---
    st.markdown("### 📝 Introduce una consulta SQL:")
    consulta = st.text_area(
        "Consulta SQL:",
        value=st.session_state.get("consulta_sql", "SELECT * FROM anuncios LIMIT 10;"),
        key="consulta_sql_area"
    )

    if st.button("Ejecutar"):
        resultados = ejecutar_sql(ruta_bd, consulta)
        if resultados is not None:
            # Eliminar columnas irrelevantes si están (como "metros")
            for col in ["metros", "superficie"]:
                if col in resultados.columns:
                    resultados.drop(columns=[col], inplace=True)
            columnas_no_vacias = [col for col in resultados.columns if not resultados[col].isna().all()]
            resultados = resultados[columnas_no_vacias]
            st.success(f"✅ Consulta ejecutada con éxito. {len(resultados)} filas obtenidas.")
            st.dataframe(resultados)

    # --- Mostrar imagen al final ---
    st.markdown("---")
    mostrar_imagen_bd(tipo)
