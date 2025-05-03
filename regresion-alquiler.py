#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
regresion_alquiler.py

Preprocesamiento, entrenamiento y evaluación de un modelo LightGBM
para predecir rentas de alquiler a partir de características del inmueble.
"""

import os
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error

import joblib
from lightgbm import LGBMRegressor


def main():
    # Limitar threads en OpenMP / LightGBM
    os.environ["OMP_NUM_THREADS"] = "3"

    # ---------------------------------------------------------------------
    # 1. Cargar datos desde ruta absoluta en macOS
    # ---------------------------------------------------------------------
    ruta_csv = Path.home() / "Documents" / "GitHub" / "proyecto pisos" / "app pisos" / "data" / "alquiler.csv"
    print(f"Intentando leer CSV en: {ruta_csv.resolve()}")
    if not ruta_csv.exists():
        raise FileNotFoundError(f"No se encontró el archivo de datos: {ruta_csv}")
    df = pd.read_csv(ruta_csv, encoding="utf-8")

    # ---------------------------------------------------------------------
    # 2. Filtrar y limpiar datos
    # ---------------------------------------------------------------------
    min_price, max_price = 200, 10000
    df = df.dropna(subset=["precio", "habitaciones", "baños", "superficie_construida"])
    df = df[(df["precio"] >= min_price) & (df["precio"] <= max_price)]

    # Rellenar precio por m² si falta
    if "precio_m2" in df.columns:
        df["precio_m2"] = df["precio_m2"].fillna(df["precio_m2"].mean())

    # ---------------------------------------------------------------------
    # 3. Eliminar filas sin coordenadas y clustering geográfico
    # ---------------------------------------------------------------------
    df = df.dropna(subset=["lat", "lon"])
    df["cluster"] = KMeans(n_clusters=5, random_state=42).fit_predict(df[["lat", "lon"]])

    # ---------------------------------------------------------------------
    # 4. Variables categóricas
    # ---------------------------------------------------------------------
    cat_cols = ["conservacion"] if "conservacion" in df.columns else []
    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    encoded_cat = encoder.fit_transform(df[cat_cols]) if cat_cols else np.empty((len(df), 0))
    encoded_cols = encoder.get_feature_names_out(cat_cols) if cat_cols else []

    type_cols = [c for c in [
        "piso", "casa", "atico", "estudio", "apartamento",
        "duplex", "chalet", "finca", "loft"
    ] if c in df.columns]

    # ---------------------------------------------------------------------
    # 5. Construir matriz de features
    # ---------------------------------------------------------------------
    X_base = df[[
        "habitaciones", "baños", "superficie_construida",
        "precio_m2", "lat", "lon", "cluster"
    ]].copy()
    X_base["habitaciones_por_m2"] = df["habitaciones"] / (df["superficie_construida"] + 1)
    X_base["densidad"] = df["superficie_construida"] / (df["baños"] + 1)

    X = pd.concat([
        X_base.reset_index(drop=True),
        df[type_cols].reset_index(drop=True),
        pd.DataFrame(encoded_cat, columns=encoded_cols)
    ], axis=1)
    y = df["precio"]

    # ---------------------------------------------------------------------
    # 6. Escalado y guardado de scaler/encoder
    # ---------------------------------------------------------------------
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    joblib.dump(scaler, output_dir / "scaler_alquiler.pkl")
    joblib.dump(encoder, output_dir / "encoder_alquiler.pkl")

    # ---------------------------------------------------------------------
    # 7. Split y entrenamiento
    # ---------------------------------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )
    modelo = LGBMRegressor(n_estimators=300, learning_rate=0.05, max_depth=6, random_state=42)
    modelo.fit(X_train, y_train)

    # ---------------------------------------------------------------------
    # 8. Evaluación y guardado del modelo
    # ---------------------------------------------------------------------
    y_pred = modelo.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mape = mean_absolute_percentage_error(y_test, y_pred)
    print(f"MAE (LightGBM alquiler): {mae:.2f} €")
    print(f"MAPE (LightGBM alquiler): {mape * 100:.2f}%")
    joblib.dump(modelo, output_dir / "modelo_lightgbm_alquiler.pkl")

    # ---------------------------------------------------------------------
    # 9. Importancia de variables
    # ---------------------------------------------------------------------
    importancias = modelo.feature_importances_
    plt.figure(figsize=(10, 6))
    sns.barplot(x=importancias, y=X.columns)
    plt.title("Importancia de variables (LightGBM)")
    plt.xlabel("Importancia")
    plt.tight_layout()
    plt.savefig(output_dir / "feature_importances.png")
    plt.show()

    # ---------------------------------------------------------------------
    # 10. MAE por tipo de vivienda
    # ---------------------------------------------------------------------
    if type_cols:
        print("\nMAE por tipo de vivienda:")