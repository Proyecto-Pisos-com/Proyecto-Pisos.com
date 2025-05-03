from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib

def main():
    # 1) Definir ruta base del proyecto (ajustada a tu estructura)
    PROJECT_ROOT = Path.home() / "Documents" / "GitHub" / "Proyecto-Pisos.com"
    data_csv    = PROJECT_ROOT / "app_pisos" / "data" / "alquiler.csv"
    output_dir  = PROJECT_ROOT / "app_pisos" / "output"
    output_dir.mkdir(exist_ok=True, parents=True)

    # 2) Cargar datos
    if not data_csv.exists():
        raise FileNotFoundError(f"No se encontró el CSV en: {data_csv}")
    df = pd.read_csv(data_csv, encoding="utf-8")

    # 3) Limpieza y filtro
    df = df.dropna(subset=["precio", "superficie_construida"])
    df = df[(df["precio"] >= 200) & (df["precio"] <= 10000)]
    df["precio_m2"] = df["precio"] / df["superficie_construida"]

    # 4) Crear etiqueta de segmento según percentiles
    cutoffs = np.percentile(df["precio_m2"], [33, 66])
    def segmento(p):
        if p <= cutoffs[0]: return 0  # bajo
        if p <= cutoffs[1]: return 1  # medio
        return 2                       # alto
    df["price_segment"] = df["precio_m2"].apply(segmento)

    # 5) Preparar X e y
    features = ["habitaciones", "baños", "superficie_construida", "precio_m2", "lat", "lon"]
    X = df[features].fillna(0)
    y = df["price_segment"]

    # 6) Train/test split con estratificación
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # 7) Escalado
    scaler    = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s  = scaler.transform(X_test)

    # 8) Guardar el escalador
    scaler_path = output_dir / "scaler_segmento_precio.pkl"
    joblib.dump(scaler, scaler_path)
    print(f"Escalador guardado en: {scaler_path}")

    # 9) Entrenar clasificador
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train_s, y_train)
    acc = clf.score(X_test_s, y_test)
    print(f"Accuracy en test: {acc*100:.2f}%")

    # 10) Guardar el modelo
    model_path = output_dir / "clf_segmento_precio.pkl"
    joblib.dump(clf, model_path)
    print(f"Modelo guardado en: {model_path}")

if __name__ == "__main__":
    main()