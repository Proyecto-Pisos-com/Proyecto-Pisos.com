#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.metrics import (mean_absolute_error, mean_absolute_percentage_error,
                             accuracy_score, classification_report)
import joblib
from lightgbm import LGBMRegressor, LGBMClassifier


def main():
    # Limitar hilos para LightGBM/OpenMP
    os.environ["OMP_NUM_THREADS"] = "3"

    # 1. Lectura de datos
    base_path = Path.home() / "Documents" / "GitHub" / "Proyecto-Pisos.com"
    csv_path = base_path / "app pisos" / "data" / "alquiler.csv"
    print("Leyendo datos desde:", csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"No encuentro el archivo: {csv_path}")
    df = pd.read_csv(csv_path, encoding="utf-8")
    print(f"Registros cargados: {len(df)}")

    # 2. Limpieza y filtrado
    df = df.dropna(subset=["precio", "habitaciones", "baños", "superficie_construida"])
    min_price, max_price = 200, 10000
    df = df[(df["precio"] >= min_price) & (df["precio"] <= max_price)]
    print(f"Después de la limpieza: {len(df)} registros")

    # 3. Feature engineering
    if "precio_m2" in df.columns:
        df["precio_m2"] = df["precio_m2"].fillna(df["precio_m2"].mean())
    df = df.dropna(subset=["lat", "lon"])

    # Clustering geográfico
    df["cluster"] = KMeans(n_clusters=5, random_state=42).fit_predict(df[["lat", "lon"]])

    # One-hot para conservacion y dummies para tipo de vivienda
    cat_cols = ["conservacion"] if "conservacion" in df.columns else []
    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    encoded_cat = encoder.fit_transform(df[cat_cols]) if cat_cols else np.empty((len(df), 0))
    encoded_cols = encoder.get_feature_names_out(cat_cols) if cat_cols else []
    tipo_cols = [c for c in ["piso", "casa", "atico", "estudio", "apartamento", "duplex", "chalet", "finca", "loft"] if c in df.columns]

    # Matriz de features X
    X_base = df[["habitaciones", "baños", "superficie_construida", "precio_m2", "lat", "lon"]].copy()
    X_base["hab_por_m2"] = df["habitaciones"] / (df["superficie_construida"] + 1)
    X_base["densidad"] = df["superficie_construida"] / (df["baños"] + 1)
    X = pd.concat([
        X_base.reset_index(drop=True),
        df[tipo_cols].reset_index(drop=True),
        pd.DataFrame(encoded_cat, columns=encoded_cols)
    ], axis=1)
    y_reg = df["precio"]
    y_clust = df["cluster"]
    print("Dimensiones de X:", X.shape)

    # 4. División de datos en train y test
    X_train, X_test, y_train_reg, y_test_reg = train_test_split(
        X, y_reg, test_size=0.2, random_state=42)
    # Para clasificación de clusters usamos la misma partición
    _, _, y_train_clust, y_test_clust = train_test_split(
        X, y_clust, test_size=0.2, random_state=42)
    print(f"Train: {X_train.shape[0]} muestras, Test: {X_test.shape[0]} muestras")

    # 5. Escalado (ajuste solo en train)
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    output_dir = base_path / "app pisos" / "output"
    output_dir.mkdir(exist_ok=True)
    joblib.dump(scaler, output_dir / "scaler_alquiler.pkl")
    joblib.dump(encoder, output_dir / "encoder_alquiler.pkl")

    # 6. Regresión con LightGBM
    reg_model = LGBMRegressor(n_estimators=200, learning_rate=0.05, max_depth=6, random_state=42)
    reg_model.fit(X_train_scaled, y_train_reg)
    y_pred_reg = reg_model.predict(X_test_scaled)
    mae = mean_absolute_error(y_test_reg, y_pred_reg)
    mape = mean_absolute_percentage_error(y_test_reg, y_pred_reg)
    print(f"MAE regresión: {mae:.2f} € | MAPE: {mape*100:.2f}%")
    joblib.dump(reg_model, output_dir / "modelo_lgbm_alquiler.pkl")

    # 7. Clasificación de clusters
    clf_model = LGBMClassifier(n_estimators=100, learning_rate=0.1, max_depth=6, random_state=42)
    clf_model.fit(X_train_scaled, y_train_clust)
    y_pred_clust = clf_model.predict(X_test_scaled)
    acc = accuracy_score(y_test_clust, y_pred_clust)
    print(f"Accuracy clasificación clusters: {acc*100:.2f}%")
    print(classification_report(y_test_clust, y_pred_clust))
    joblib.dump(clf_model, output_dir / "clf_clusters.pkl")

    # 8. Importancias de la clasificación
    feat_names = X.columns
    importances_clf = clf_model.feature_importances_
    plt.figure(figsize=(8,6))
    sns.barplot(x=importances_clf, y=feat_names)
    plt.title("Importancia de variables - Clasificación de Clusters")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
