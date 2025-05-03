
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from lightgbm import LGBMRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

def main():
    # Rutas
    ROOT       = Path(__file__).resolve().parent
    data_csv   = ROOT / "app_pisos" / "data" / "alquiler.csv"
    models_dir = ROOT / "models"
    models_dir.mkdir(exist_ok=True)

    # 1) Carga y limpieza
    if not data_csv.exists():
        raise FileNotFoundError(f"No se encontró CSV en {data_csv}")
    df = pd.read_csv(data_csv)
    df = df.dropna(subset=["precio","habitaciones","baños","superficie_construida","lat","lon"])
    df = df[(df["precio"]>=200)&(df["precio"]<=10000)]
    df["precio_m2"] = df["precio"]/df["superficie_construida"]

    # 2) Clustering geográfico
    df["cluster"] = KMeans(n_clusters=5, random_state=42).fit_predict(df[["lat","lon"]])

    # 3) Preparar features y target de regresión
    features = ["habitaciones","baños","superficie_construida","precio_m2","lat","lon","cluster"]
    X = df[features]
    y = df["precio"]

    # 4) Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 5) Escalado
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s  = scaler.transform(X_test)

    # 6) Entrenar regresión
    reg = LGBMRegressor(n_estimators=300, learning_rate=0.05, max_depth=6, random_state=42)
    reg.fit(X_train_s, y_train)

    # 7) Guardar artefactos de regresión
    scaler_path = models_dir / "scaler_alquiler.pkl"
    model_path  = models_dir / "modelo_lgbm_alquiler.pkl"
    joblib.dump(scaler, scaler_path)
    joblib.dump(reg,   model_path)
    print(f"Regresión guardada en models/: {scaler_path.name}, {model_path.name}")

    # 8) Predecir y etiquetar deals sobre TODO el dataset
    X_all_s = scaler.transform(X.fillna(0))
    preds   = reg.predict(X_all_s)
    df["dev_rel"] = (df["precio"] - preds) / preds
    df["deal_label"] = df["dev_rel"].apply(
        lambda d: "Chollo"    if d < -0.10 
                  else "Sobreprecio" if d >  0.10 
                  else "Justo"
    )

    # 9) Entrenar clasificador de deals
    le  = LabelEncoder()
    y_d = le.fit_transform(df["deal_label"])
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_all_s, y_d)

    # 10) Guardar artefactos de deals
    clf_path = models_dir / "clf_deal.pkl"
    le_path  = models_dir / "le_deal.pkl"
    joblib.dump(clf, clf_path)
    joblib.dump(le,  le_path)
    print(f"Deals guardados en models/: {clf_path.name}, {le_path.name}")

if __name__ == "__main__":
    main()