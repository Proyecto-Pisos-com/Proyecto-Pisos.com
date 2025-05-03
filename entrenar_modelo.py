import pickle
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder

def preparar_datos(df, columnas_usar):
    """Convierte datos categóricos a numéricos y prepara el dataset para el modelo."""
    columnas_categoricas = ["conservacion", "tipo_vivienda"]
    
    for col in columnas_categoricas:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
    
    # Eliminar valores nulos
    df_model = df.dropna(subset=columnas_usar + ["precio"])
    
    X = df_model[columnas_usar]
    y = df_model["precio"]

    return X, y

def entrenar_modelo(df, columnas_usar):
    """Entrena un modelo de red neuronal para predecir el precio de viviendas."""
    X, y = preparar_datos(df, columnas_usar)
    
    # Dividir los datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Definir y entrenar el modelo
    modelo = MLPRegressor(hidden_layer_sizes=(50, 50), max_iter=1000, random_state=42)
    modelo.fit(X_train, y_train)

    # Predicción y evaluación
    predicciones = modelo.predict(X_test)
    mse = mean_squared_error(y_test, predicciones)

    return modelo, predicciones, y_test, mse


