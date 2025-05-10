import os
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
import joblib
from lightgbm import LGBMRegressor


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

    # 2. Limpieza y filtrado inicial
    df = df.dropna(subset=["precio", "habitaciones", "baños", "superficie_construida"])
    min_price, max_price = 200, 10000
    df = df[(df["precio"] >= min_price) & (df["precio"] <= max_price)]
    print(f"Después de la limpieza: {len(df)} registros")

    # 3. Feature engineering básico
    if "precio_m2" in df.columns:
        df["precio_m2"] = df["precio_m2"].fillna(df["precio_m2"].mean())
    df = df.dropna(subset=["lat", "lon"])
    df["cluster"] = KMeans(n_clusters=5, random_state=42).fit_predict(df[["lat", "lon"]])

    cat_cols = ["conservacion"] if "conservacion" in df.columns else []
    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    encoded_cat = encoder.fit_transform(df[cat_cols]) if cat_cols else np.empty((len(df), 0))
    encoded_cols = encoder.get_feature_names_out(cat_cols) if cat_cols else []

    tipo_cols = [c for c in ["piso", "casa", "atico", "estudio", "apartamento", "duplex", "chalet", "finca", "loft"] if c in df.columns]

    X_base = df[["habitaciones", "baños", "superficie_construida", "precio_m2", "lat", "lon", "cluster"]].copy()
    X_base["hab_por_m2"] = df["habitaciones"] / (df["superficie_construida"] + 1)
    X_base["densidad"] = df["superficie_construida"] / (df["baños"] + 1)

    X = pd.concat([
        X_base.reset_index(drop=True),
        df[tipo_cols].reset_index(drop=True),
        pd.DataFrame(encoded_cat, columns=encoded_cols)
    ], axis=1)
    y = df["precio"]
    print("Dimensiones de X:", X.shape)

    # 4. División de datos en train y test (sin escalar aún)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Conjunto de entrenamiento: {X_train.shape[0]} muestras")
    print(f"Conjunto de prueba: {X_test.shape[0]} muestras")

    # 5. Escalado de variables (usar solo datos de entrenamiento para el ajuste)
    # Elegir escalador: StandardScaler o MinMaxScaler
    scaler = StandardScaler()
    # scaler = MinMaxScaler(feature_range=(0,1))
    
    # Ajustar scaler solo con X_train
    scaler.fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Guardar el escalador para producción
    output_dir = base_path / "app pisos" / "output"
    output_dir.mkdir(exist_ok=True)
    scaler_path = output_dir / "scaler_alquiler.pkl"
    joblib.dump(scaler, scaler_path)
    print("Escalador guardado en:", scaler_path)

    # 6. Entrenamiento del modelo LightGBM
    modelo = LGBMRegressor(n_estimators=200, learning_rate=0.05, max_depth=6, random_state=42)
    modelo.fit(X_train_scaled, y_train)

    # 7. Evaluación del modelo
    y_pred = modelo.predict(X_test_scaled)
    mae = mean_absolute_error(y_test, y_pred)
    mape = mean_absolute_percentage_error(y_test, y_pred)
    print(f"MAE final: {mae:.2f} €")
    print(f"MAPE final: {mape*100:.2f}%")

    # Guardar el modelo entrenado
    model_path = output_dir / "modelo_lgbm_alquiler.pkl"
    joblib.dump(modelo, model_path)
    print("Modelo guardado en:", model_path)

    # 8. Importancia de variables
    importancias = modelo.feature_importances_
    plt.figure(figsize=(8,6))
    sns.barplot(x=importancias, y=X.columns)
    plt.title("Importancia de variables")
    plt.tight_layout()
    plt.show()

    # 9. MAE por tipo de vivienda
    if tipo_cols:
        print("\nMAE por tipo de vivienda:")
        for t in tipo_cols:
            subset = df[df[t] == 1]
            if len(subset) >= 10:
                X_sub = subset[X.columns]
                X_sub_scaled = scaler.transform(X_sub)
                y_sub = subset["precio"]
                y_pred_sub = modelo.predict(X_sub_scaled)
                error = mean_absolute_error(y_sub, y_pred_sub)
                print(f"- {t}: MAE={error:.2f} €")

if __name__ == "__main__":
    main()
