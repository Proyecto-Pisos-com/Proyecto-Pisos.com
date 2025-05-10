import pandas as pd
from sklearn.preprocessing import LabelEncoder

def load_data():
    df = pd.read_csv("ventas.csv")

    # Codificar 'tipo_vivienda'
    label_encoder = LabelEncoder()
    df["tipo_vivienda_encoded"] = label_encoder.fit_transform(df["tipo_vivienda"])

    return df

