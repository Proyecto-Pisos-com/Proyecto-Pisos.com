import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from utils import cargar_datos

import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def show_calculadora_compra():
    # --- Cargar datos ---
    @st.cache_data
    def cargar_filtrados():
        df = cargar_datos("ventas.csv")
        return df.dropna(subset=["titulo", "lat", "lon", "precio"])

    df = cargar_filtrados()

    st.title("🏡 Ficha Detallada del Inmueble en Venta")

    # Selector
    titulos = df["titulo"].drop_duplicates().tolist()
    titulo_seleccionado = st.selectbox("Selecciona un inmueble", options=titulos)

    inmueble = df[df["titulo"] == titulo_seleccionado].iloc[0]

    # --- Mostrar detalles ---
    st.subheader(inmueble["titulo"])
    st.markdown(f"**Ubicación:** {inmueble.get('ubicacion', 'No disponible')}")
    st.markdown(f"**Precio:** {int(inmueble['precio'])} €")
    st.markdown(f"**Precio por m²:** {int(inmueble['precio_m2']) if pd.notna(inmueble['precio_m2']) else 'No disponible'} €")
    st.markdown(f"**Conservación:** {inmueble.get('conservacion', 'No disponible')}")
    st.markdown(f"**Habitaciones:** {int(inmueble['habitaciones']) if pd.notna(inmueble['habitaciones']) else 'No disponible'}")
    st.markdown(f"**Baños:** {int(inmueble['baños']) if pd.notna(inmueble['baños']) else 'No disponible'}")
    st.markdown(f"**Superficie construida:** {int(inmueble['superficie_construida']) if pd.notna(inmueble['superficie_construida']) else 'No disponible'} m²")
    st.markdown(f"[Ver publicación original]({inmueble['link']})")

    # --- Mapa ---
    st.subheader("📍 Ubicación exacta")
    m = folium.Map(location=[inmueble["lat"], inmueble["lon"]], zoom_start=15)
    folium.Marker(
        location=[inmueble["lat"], inmueble["lon"]],
        popup=inmueble["titulo"]
    ).add_to(m)
    st_folium(m, width=700)

    # --- Calculadora de compra ---
    st.subheader("🧮 Simula tu hipoteca para este inmueble")

    precio_vivienda = int(inmueble['precio'])
    st.text_input("💰 Precio del inmueble", f"{precio_vivienda:,.0f} €", disabled=True)

    ahorros = st.number_input("💼 Tus ahorros (€)", min_value=0, value=40000, step=1000)
    plazo_anos = st.slider("📆 Plazo del préstamo (años)", min_value=5, max_value=30, value=25)
    interes = st.slider("📈 Interés anual (%)", min_value=0.5, max_value=5.0, value=2.5, step=0.1)

    prestamo = max(precio_vivienda - ahorros, 0)
    interes_mensual = interes / 100 / 12
    total_meses = plazo_anos * 12

    if prestamo > 0 and interes_mensual > 0:
        cuota = prestamo * interes_mensual / (1 - (1 + interes_mensual) ** -total_meses)
        coste_total = cuota * total_meses
        coste_con_gastos = coste_total * 1.12  # 12% de gastos
    else:
        cuota = 0
        coste_con_gastos = 0

    col1, col2 = st.columns(2)
    col1.metric("💳 Cuota mensual estimada", f"{cuota:,.2f} €")
    col2.metric("💸 Coste total aprox.", f"{coste_con_gastos:,.2f} €")

    st.caption("El cálculo incluye intereses + ~12% de gastos (notaría, impuestos, gestoría, etc.)")

    # --- Exportar CSV ---
    st.markdown("### 📥 Descargar simulación en CSV")
    df_simulacion = pd.DataFrame([{
        "Inmueble": inmueble["titulo"],
        "Ubicación": inmueble["ubicacion"],
        "Precio": precio_vivienda,
        "Ahorros": ahorros,
        "Plazo (años)": plazo_anos,
        "Interés (%)": interes,
        "Cuota mensual (€)": round(cuota, 2),
        "Coste total estimado (€)": round(coste_con_gastos, 2)
    }])
    csv_buffer = io.StringIO()
    df_simulacion.to_csv(csv_buffer, index=False, sep=";")
    st.download_button(
        label="💾 Descargar CSV",
        data=csv_buffer.getvalue(),
        file_name=f"simulacion_{titulo_seleccionado.replace(' ', '_')}.csv",
        mime="text/csv"
    )

    # --- Exportar PDF ---
    st.markdown("### 📄 Descargar simulación en PDF")

    def generar_pdf():
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        text = c.beginText(50, 800)
        text.setFont("Helvetica", 11)
        text.textLine("Resumen de simulación hipotecaria:")
        text.textLine("")
        for key, val in df_simulacion.iloc[0].items():
            text.textLine(f"{key}: {val}")
        c.drawText(text)
        c.showPage()
        c.save()
        buffer.seek(0)
        return buffer

    pdf = generar_pdf()

    st.download_button(
        label="📄 Descargar PDF",
        data=pdf,
        file_name=f"simulacion_{titulo_seleccionado.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )

