#!/usr/bin/env python3
# train_alquiler_models.py

"""
Este script entrena y guarda todos los artefactos necesarios para tu app:
  • KMeans geográfico (5 clusters)
  • StandardScaler
  • LightGBMRegressor
  • DecisionTreeClassifier + LabelEncoder para chollos/sobreprecio
Los archivos .pkl resultantes se colocan en la carpeta models/.
"""

import joblib
from pathlib import Path
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from lightgbm import LGBMRegressor
from sklearn.tree import DecisionTreeClassifier

def main():
    # --- 1) Definir rutas ---
    ROOT        = Path(__file__).resolve().parent
    # Primero busca el CSV en App_Pisos/app/data/, si no existe lo toma de la raíz
    csv_in_data = ROOT / "App_Pisos" / "app" / "data" / "alquiler.csv"
    csv_in_root = ROOT / "alquiler.csv"
    if csv_in_data.exists():
        DATA_CSV = csv_in_data
    elif csv_in_root.exists():
        DATA_CSV = csv_in_root
    else:
        raise FileNotFoundError(
            f"No encuentro alquiler.csv en:\n"
            f"  {csv_in_data}\n"
            f"  {csv_in_root}"
        )
    MODELS_DIR = ROOT / "models"
    MODELS_DIR.mkdir(exist_ok=True)

    print(f"Cargando datos desde: {DATA_CSV}")
    df = pd.read_csv(DATA_CSV)
    # --- 2) Limpieza básica ---
    df = df.dropna(subset=["precio","habitaciones","baños","superficie_construida","lat","lon"])
    df = df[df.precio.between(200, 10000)]
    df["precio_m2"] = df.precio / df.superficie_construida

    # --- 3) Entrenar KMeans geográfico ---
    km = KMeans(n_clusters=5, random_state=42).fit(df[["lat","lon"]])
    joblib.dump(km, MODELS_DIR / "kmeans_alquiler.pkl")
    print("✔ Guardado models/kmeans_alquiler.pkl")

    # Añadimos la etiqueta de cluster al DataFrame
    df["cluster"] = km.labels_

    # --- 4) Preparar X,y para regresión ---
    features = ["habitaciones","baños","superficie_construida","precio_m2","lat","lon","cluster"]
    X, y = df[features], df["precio"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # --- 5) Escalado ---
    scaler = StandardScaler().fit(X_train)
    joblib.dump(scaler, MODELS_DIR / "scaler_alquiler.pkl")
    print("✔ Guardado models/scaler_alquiler.pkl")
    X_train_s = scaler.transform(X_train)
    X_test_s  = scaler.transform(X_test)

    # --- 6) Entrenar LightGBMRegressor ---
    reg = LGBMRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        random_state=42
    )
    reg.fit(X_train_s, y_train)
    joblib.dump(reg, MODELS_DIR / "modelo_lgbm_alquiler.pkl")
    print("✔ Guardado models/modelo_lgbm_alquiler.pkl")

    # --- 7) Calcular desviaciones y etiquetas “deal” en todo el set ---
    X_all_s   = scaler.transform(X)
    preds_all = reg.predict(X_all_s)
    df["dev_rel"] = (df["precio"] - preds_all) / preds_all
    df["deal_label"] = df["dev_rel"].apply(
        lambda d: "Chollo"     if d < -0.10
                  else "Sobreprecio" if d >  0.10
                  else "Justo"
    )

    # --- 8) Entrenar DecisionTreeClassifier para “deal” ---
    le  = LabelEncoder().fit(df.deal_label)
    y_d = le.transform(df.deal_label)
    clf = DecisionTreeClassifier(random_state=42).fit(X_all_s, y_d)
    joblib.dump(clf, MODELS_DIR / "clf_deal.pkl")
    joblib.dump(le,  MODELS_DIR / "le_deal.pkl")
    print("✔ Guardado models/clf_deal.pkl y models/le_deal.pkl")

    print("\n🎉 Todos los modelos y transformadores están en la carpeta `models/`.")

if __name__ == "__main__":
    main()
