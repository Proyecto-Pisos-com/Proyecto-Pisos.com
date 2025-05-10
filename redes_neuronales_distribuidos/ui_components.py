import streamlit as st
import numpy as np

def show_filters(df, model, scaler_X, scaler_y):
    st.sidebar.header("🔍 Datos de la Vivienda")

    titulo = st.sidebar.selectbox("Título de la vivienda", df["titulo"].unique())
    ubicacion = st.sidebar.selectbox("Ubicación", df["ubicacion"].unique())

    habitaciones = st.sidebar.selectbox("Habitaciones", list(range(1, 11)))
    banos = st.sidebar.selectbox("Baños", list(range(1, 6)))
    superficie_util = st.sidebar.selectbox("Superficie útil (m²)", list(range(30, 301)))

    tipo_vivienda = st.sidebar.selectbox("Tipo de vivienda", df["tipo_vivienda"].unique())
    tipo_vivienda_encoded = df[df["tipo_vivienda"] == tipo_vivienda]["tipo_vivienda_encoded"].iloc[0]

    precio_predicho_deseescalado = None
    precio_real = None
    diferencia_precio = None
    vivienda_lat, vivienda_lon = None, None

    if st.sidebar.button("🔮 Predecir precio"):
        input_data = np.array([[habitaciones, banos, superficie_util, tipo_vivienda_encoded]])
        input_data_scaled = scaler_X.transform(input_data)

        precio_predicho_scaled = model.predict(input_data_scaled)
        precio_predicho_deseescalado = scaler_y.inverse_transform(precio_predicho_scaled.reshape(-1, 1))[0][0]

        # Obtener el precio real de la vivienda seleccionada
        vivienda = df.loc[(df["habitaciones"] == habitaciones) &
                          (df["baños"] == banos) &
                          (df["superficie_util"] == superficie_util) &
                          (df["tipo_vivienda"] == tipo_vivienda)]

        if not vivienda.empty:
            precio_real = vivienda.iloc[0]["precio"]
            vivienda_lat, vivienda_lon = vivienda.iloc[0]["lat"], vivienda.iloc[0]["lon"]

            # Calcular la diferencia entre el precio real y el precio predicho
            diferencia_precio = abs(precio_real - precio_predicho_deseescalado)

        # Mostrar resultados en la interfaz
        st.subheader(f"💰 Precio predicho: {precio_predicho_deseescalado:,.2f} €")
        
        if precio_real is not None:
            st.subheader(f"🏠 Precio real: {precio_real:,.2f} €")
            st.subheader(f"🔎 Diferencia entre precios: {diferencia_precio:,.2f} €")

    return precio_predicho_deseescalado, precio_real, diferencia_precio, vivienda_lat, vivienda_lon

