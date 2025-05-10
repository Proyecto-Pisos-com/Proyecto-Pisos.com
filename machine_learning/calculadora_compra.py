import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import r2_score, mean_absolute_error
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import shap
import matplotlib.pyplot as plt
from utils import cargar_datos
from config import VENTAS_CSV, MODELO_LIGHTGBM_VENTAS, SCALER_VENTAS

@st.cache_data
def calcular_precision_modelo(df, _modelo, _scaler):
    df_valid = df.dropna(subset=[
        "habitaciones", "baños", "superficie_construida", "precio_m2",
        "lat", "lon", "conservacion", "tipo_vivienda", "precio"
    ])

    tipo_cols = ["piso", "casa", "atico", "estudio", "apartamento", "duplex", "chalet", "finca", "loft"]
    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    encoder.fit(df_valid[["conservacion"]].fillna("Desconocido"))

    df_valid["cluster"] = KMeans(n_clusters=5, random_state=42).fit_predict(df_valid[["lat", "lon"]])
    df_valid["habitaciones_por_m2"] = df_valid["habitaciones"] / (df_valid["superficie_construida"] + 1)
    df_valid["densidad"] = df_valid["superficie_construida"] / (df_valid["baños"] + 1)

    tipo_df = pd.DataFrame([{col: 1 if str(row["tipo_vivienda"]).lower() == col else 0 for col in tipo_cols} for _, row in df_valid.iterrows()])
    conservacion_df = pd.DataFrame(
        encoder.transform(df_valid[["conservacion"]].fillna("Desconocido")),
        columns=encoder.get_feature_names_out()
    )

    X = pd.concat([
        df_valid[["habitaciones", "baños", "superficie_construida", "precio_m2", "lat", "lon", "cluster", "habitaciones_por_m2", "densidad"]],
        tipo_df.reset_index(drop=True),
        conservacion_df.reset_index(drop=True)
    ], axis=1)

    y = df_valid["precio"]
    X = X[_scaler.feature_names_in_]
    X_scaled = _scaler.transform(X)
    y_pred = _modelo.predict(X_scaled)

    r2 = r2_score(y, y_pred)
    mae = mean_absolute_error(y, y_pred)

    return r2, mae

def show_calculadora_compra():
    @st.cache_data
    def cargar_filtrados():
        df = cargar_datos(VENTAS_CSV)
        return df.dropna(subset=["titulo", "lat", "lon", "precio"])

    df = cargar_filtrados()

    st.markdown("### 🔎 Buscar inmueble")
    col_selector, _ = st.columns([1, 5])
    with col_selector:
        titulo_seleccionado = st.selectbox("Selecciona un inmueble", options=df["titulo"].drop_duplicates().tolist())

    inmueble = df[df["titulo"] == titulo_seleccionado].iloc[0]

    col_izq, col_der = st.columns([3, 2])
    with col_izq:
        st.title("🏡 Ficha Detallada del Inmueble en Venta")
        st.subheader(inmueble["titulo"])
        st.markdown(f"**Precio:** {int(inmueble['precio']):,} €")
        st.markdown(f"**Precio por m²:** {int(inmueble['precio_m2']) if pd.notna(inmueble['precio_m2']) else 'No disponible'} €")
        st.markdown(f"**Conservación:** {inmueble.get('conservacion', 'No disponible')}")
        st.markdown(f"**Habitaciones:** {int(inmueble['habitaciones'])}")
        st.markdown(f"**Baños:** {int(inmueble['baños'])}")
        st.markdown(f"**Superficie construida:** {int(inmueble['superficie_construida'])} m²")
        st.markdown(f"[Ver publicación original]({inmueble['link']})")

    with col_der:
        st.markdown("📍 **Ubicación**")
        st.markdown(f"**Zona:** {inmueble.get('ubicacion', 'No disponible')}")
        m = folium.Map(location=[inmueble["lat"], inmueble["lon"]], zoom_start=15, tiles="CartoDB dark_matter")
        folium.Marker(location=[inmueble["lat"], inmueble["lon"]], popup=inmueble["titulo"], icon=folium.Icon(color="green")).add_to(m)
        st_folium(m, use_container_width=True, height=450)

    st.subheader("🤖 Estimación de Precio de Venta")
    modelo = joblib.load(MODELO_LIGHTGBM_VENTAS)
    scaler = joblib.load(SCALER_VENTAS)

    habitaciones = int(inmueble['habitaciones'])
    baños = int(inmueble['baños'])
    superficie_construida = int(inmueble['superficie_construida'])
    tipo = inmueble.get("tipo_vivienda", "Piso")
    conservacion = inmueble.get("conservacion", "Desconocido")
    lat = inmueble["lat"]
    lon = inmueble["lon"]

    df_precio = df.copy()
    df_precio['dist'] = np.sqrt((df_precio['lat'] - lat)**2 + (df_precio['lon'] - lon)**2)
    precio_m2 = df_precio[df_precio['dist'] < 0.02]['precio_m2'].mean()
    if pd.isna(precio_m2): precio_m2 = 0

    tipo_cols = ["piso", "casa", "atico", "estudio", "apartamento", "duplex", "chalet", "finca", "loft"]
    tipo_dict = {col: 1 if tipo.lower() == col else 0 for col in tipo_cols}

    df_cluster = df[["lat", "lon"]].dropna()
    kmeans = KMeans(n_clusters=5, random_state=42).fit(df_cluster)
    cluster = int(kmeans.predict([[lat, lon]])[0])

    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    encoder.fit(df[["conservacion"]].fillna("Desconocido"))
    encoded_input = encoder.transform([[conservacion]])

    habitaciones_por_m2 = habitaciones / (superficie_construida + 1)
    densidad = superficie_construida / (baños + 1)

    entrada = pd.DataFrame([[habitaciones, baños, superficie_construida, precio_m2, lat, lon, cluster,
                              habitaciones_por_m2, densidad]],
                            columns=["habitaciones", "baños", "superficie_construida", "precio_m2", "lat", "lon", "cluster",
                                     "habitaciones_por_m2", "densidad"])
    tipo_df = pd.DataFrame([tipo_dict])
    conservacion_df = pd.DataFrame(encoded_input, columns=encoder.get_feature_names_out())
    entrada_full = pd.concat([entrada, tipo_df, conservacion_df], axis=1)

    entrada_full = entrada_full[scaler.feature_names_in_]
    entrada_scaled = scaler.transform(entrada_full)
    prediccion = modelo.predict(entrada_scaled)[0]
    rango_inferior = int(prediccion * 0.90)
    rango_superior = int(prediccion * 1.10)

    col1, col2 = st.columns([2, 2])
    with col1:
        st.markdown(f"### 💶 Precio estimado: **{int(prediccion):,} €**")
        st.markdown(f"📊 Intervalo estimado: Entre **{rango_inferior:,} €** y **{rango_superior:,} €**")
    with col2:
        st.markdown("### 💷 Precio real del anuncio")
        st.markdown(f"**{int(inmueble['precio']):,} €**")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Estimado", "Real"],
        y=[int(prediccion), int(inmueble['precio'])],
        marker_color=["blue", "orange"],
        text=[f"{int(prediccion):,} €", f"{int(inmueble['precio']):,} €"],
        textposition="outside"
    ))
    fig.update_layout(title="📈 Comparativa entre precio estimado y real", yaxis_title="€", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    precio_real = int(inmueble['precio'])
    if precio_real < prediccion:
        st.success(f"🚀 Oportunidad: {prediccion - precio_real:,.0f} € por debajo del valor estimado")
    elif precio_real > prediccion:
        st.error(f"⚠️ Sobreprecio: {precio_real - prediccion:,.0f} € por encima del valor estimado")

    # --- SHAP analysis ---
    st.subheader("🔬 Análisis explicativo del modelo (SHAP)")
    with st.spinner("Generando análisis explicativo..."):
        explainer = shap.Explainer(modelo)
        shap_values = explainer(pd.DataFrame(entrada_scaled, columns=entrada_full.columns))

        with st.expander("💡 ¿Qué significa este gráfico?"):
            st.markdown("""
            Este gráfico muestra cómo cada característica del inmueble (como superficie, número de baños, ubicación, etc.) ha influido en el precio estimado por el modelo de inteligencia artificial.  
            - Las barras **rosas** indican un impacto **positivo** (aumentan el precio).  
            - Las barras **azules** indican un impacto **negativo** (reducen el precio).  
            Cuanto más larga la barra, mayor es su influencia en el precio final.
            """)

        fig, ax = plt.subplots(figsize=(5, 2.5))
        shap.plots.bar(shap_values[0], max_display=10, show=False)

        for txt in ax.texts:
            txt.set_visible(False)

        plt.tight_layout()
        st.pyplot(fig)


    # --- Precision del modelo ---
    with st.expander("📊 Ver precisión del modelo de estimación"):
        r2, mae = calcular_precision_modelo(df, modelo, scaler)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📈 R² (Precisión)", f"{r2:.2f}")
        with col2:
            st.metric("📉 MAE (Error Medio)", f"{int(mae):,} €")

    # --- Simulador de hipoteca ---
    st.subheader("🧲 Simula tu hipoteca para este inmueble")
    st.text_input("💰 Precio del inmueble", f"{int(inmueble['precio']):,} €", disabled=True)

    ahorros = st.number_input("💼 Tus ahorros (€)", min_value=0, value=40000, step=1000)
    plazo_anos = st.slider("🕖️ Plazo del préstamo (años)", 5, 30, 25)
    interes = st.slider("📈 Interés anual (%)", 0.5, 5.0, 2.5, step=0.1)

    prestamo = max(int(inmueble['precio']) - ahorros, 0)
    interes_mensual = interes / 100 / 12
    total_meses = plazo_anos * 12
    cuota = prestamo * interes_mensual / (1 - (1 + interes_mensual) ** -total_meses) if prestamo > 0 else 0
    coste_con_gastos = cuota * total_meses * 1.12 if cuota > 0 else 0

    col1, col2 = st.columns(2)
    col1.metric("💳 Cuota mensual estimada", f"{cuota:,.2f} €")
    col2.metric("💸 Coste total aprox.", f"{coste_con_gastos:,.2f} €")
    st.caption("El cálculo incluye intereses + ~12% de gastos (notaría, impuestos, gestoría, etc.)")

    # --- Exportar simulación CSV ---
    st.markdown("### 🗓️ Descargar simulación en CSV")
    df_simulacion = pd.DataFrame([{
        "Inmueble": inmueble["titulo"],
        "Ubicación": inmueble["ubicacion"],
        "Precio": int(inmueble['precio']),
        "Ahorros": ahorros,
        "Plazo (años)": plazo_anos,
        "Interés (%)": interes,
        "Cuota mensual (€)": round(cuota, 2),
        "Coste total estimado (€)": round(coste_con_gastos, 2)
    }])
    csv_buffer = io.StringIO()
    df_simulacion.to_csv(csv_buffer, index=False, sep=";")
    st.download_button(
        label="📀 Descargar CSV",
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
