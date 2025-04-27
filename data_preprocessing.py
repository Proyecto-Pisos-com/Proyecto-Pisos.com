import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "alquiler.csv")

df = pd.read_csv(csv_path)

target_col = "precio"
X = df.drop(columns=[target_col])
y = df[target_col]

numeric_features = X.select_dtypes(include=["number", "bool"]).columns.tolist()
categorical_features = ["conservacion"]  # ajusta si tienes más

preprocessor = ColumnTransformer(transformers=[
    ("num", StandardScaler(), numeric_features),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
])

pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor)
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
pipeline.fit(X_train)

X_train_prepared = pipeline.transform(X_train)
X_test_prepared  = pipeline.transform(X_test)

pipeline_path = os.path.join(base_dir, "preprocessor.pkl")
with open(pipeline_path, "wb") as f:
    pickle.dump(pipeline, f)
print(f"Pipeline guardado en: {pipeline_path}")