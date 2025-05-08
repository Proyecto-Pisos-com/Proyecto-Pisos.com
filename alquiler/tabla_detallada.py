import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from utils import cargar_datos
from config import ALQUILER_CSV, VENTAS_CSV 

def show_tabla_detallada_page():
    st.title("📋 Tabla Detallada de Inmuebles")

    # --- Selección del archivo según modo ---
    modo = st.session_state.get("modo", "alquiler")
    ruta_csv = ALQUILER_CSV if modo == "alquiler" else VENTAS_CSV
    df = cargar_datos(ruta_csv) 

    if df.empty:
        st.error("⚠️ No se pudo cargar el archivo de datos.")
        return

    st.sidebar.header("🎛️ Filtros")

    if "habitaciones" in df.columns:
        df["habitaciones"] = df["habitaciones"].astype(int)
    if "baños" in df.columns:
        df["baños"] = df["baños"].astype(int)

    min_precio = int(df["precio"].min())
    max_precio = int(df["precio"].max())
    precio = st.sidebar.slider("Precio (€)", min_precio, max_precio, (min_precio, max_precio))

    habitaciones = st.sidebar.multiselect("Habitaciones", sorted(df["habitaciones"].unique()), default=sorted(df["habitaciones"].unique()))
    baños = st.sidebar.multiselect("Baños", sorted(df["baños"].unique()), default=sorted(df["baños"].unique()))

    if "metros" in df.columns:
        min_metros = int(df["metros"].min())
        max_metros = int(df["metros"].max())
        superficie = st.sidebar.slider("Superficie (m²)", min_metros, max_metros, (min_metros, max_metros))
    else:
        superficie = (0, 10000)

    df_filtrado = df[
        (df["precio"].between(*precio)) &
        (df["habitaciones"].isin(habitaciones)) &
        (df["baños"].isin(baños)) &
        (df["metros"].between(*superficie))
    ].copy()

    # Detectar tipo
    tipo_cols = [("piso", "Piso"), ("casa", "Casa"), ("atico", "Ático"), ("estudio", "Estudio"),
                 ("apartamento", "Apartamento"), ("duplex", "Dúplex"), ("chalet", "Chalet"),
                 ("finca", "Finca"), ("loft", "Loft")]

    def detectar_tipo(row):
        for col, nombre in tipo_cols:
            if col in row and row[col] == 1:
                return nombre
        return "Otro"

    df_filtrado["tipo_vivienda"] = df_filtrado.apply(detectar_tipo, axis=1)
    for col, _ in tipo_cols:
        if col in df_filtrado.columns:
            df_filtrado.drop(columns=col, inplace=True)

    # Mostrar tabla
    st.markdown(f"Se muestran **{len(df_filtrado)}** inmuebles que coinciden con los filtros.")

    st.markdown("""
        <style>
        .tabla-scroll {
            max-height: 600px;
            overflow-y: auto;
            border: 1px solid #ddd;
            padding: 10px;
            margin-top: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 8px 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        </style>
    """, unsafe_allow_html=True)

    # Eliminar columnas 'link' y 'metros' antes de mostrar la tabla
    df_visual = df_filtrado.drop(columns=["link", "metros"], errors="ignore")
    html_table = f"<div class='tabla-scroll'>{df_visual.to_html(escape=False, index=False)}</div>"

    st.markdown("📑 Tabla de inmuebles filtrados")
    st.markdown(html_table, unsafe_allow_html=True)

    # Ficha detallada
    st.markdown("---")
    st.header("📄 Ficha Detallada del Inmueble")

    titulos = df["titulo"].drop_duplicates().tolist()
    titulo_seleccionado = st.selectbox("Selecciona un inmueble", titulos)

    inmueble = df[df["titulo"] == titulo_seleccionado].iloc[0]

    col1, col2 = st.columns([1.3, 2])

    with col1:
        st.markdown("📍 Mapa de ubicación")
        m = folium.Map(location=[inmueble["lat"], inmueble["lon"]], zoom_start=15, tiles="CartoDB positron")
        folium.Marker(location=[inmueble["lat"], inmueble["lon"]], popup=inmueble["titulo"]).add_to(m)
        st_folium(m, width="100%", height=450)

    with col2:
        st.subheader(inmueble["titulo"])
        st.markdown(f"**Ubicación:** {inmueble.get('ubicacion', 'No disponible')}")
        st.markdown(f"**Precio:** {int(inmueble['precio'])} €")
        st.markdown(f"**€/m²:** {int(inmueble['precio_m2']) if pd.notna(inmueble['precio_m2']) else 'No disponible'} €")
        st.markdown(f"**Conservación:** {inmueble.get('conservacion', 'No disponible')}")
        st.markdown(f"**Habitaciones:** {int(inmueble['habitaciones'])}")
        st.markdown(f"**Baños:** {int(inmueble['baños'])}")
        st.markdown(f"**Superficie construida:** {int(inmueble['superficie_construida'])} m²")
        st.markdown(f"[Ver publicación original]({inmueble['link']})")

        if "descripcion" in inmueble and pd.notna(inmueble["descripcion"]):
            st.subheader("📝 Descripción")
            st.write(inmueble["descripcion"])
