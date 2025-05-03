import streamlit as st

def aplicar_filtros(df):
    """Aplica filtros interactivos según las columnas disponibles en el dataset."""
    st.sidebar.header("🎛️ Filtros disponibles")

    columnas_filtros = ["distrito", "ubicacion", "habitaciones", "baños", "metros", "precio", "precio_m2", "conservacion", "tipo_vivienda"]
    
    # Filtrar por columna si existe en el dataset
    for col in columnas_filtros:
        if col in df.columns and df[col].dtype == "object":  # Filtrar valores categóricos
            valores_unicos = df[col].dropna().unique()
            seleccionados = st.sidebar.multiselect(f"Filtrar por {col}:", valores_unicos, default=valores_unicos)
            df = df[df[col].isin(seleccionados)]
        elif col in df.columns and df[col].dtype in ["int64", "float64"]:  # Filtrar valores numéricos
            min_val, max_val = int(df[col].min()), int(df[col].max())
            rango_seleccionado = st.sidebar.slider(f"Rango de {col}:", min_val, max_val, (min_val, max_val))
            df = df[(df[col] >= rango_seleccionado[0]) & (df[col] <= rango_seleccionado[1])]

    return df


