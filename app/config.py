import os

# Ruta base robusta
BASE_DIR = os.path.join("C:", os.sep, "Users", "pablo", "App_Pisos", "data")

# Archivos CSV o SQLite de datos
VENTAS_CSV = os.path.join(BASE_DIR, "ventas.csv")
ALQUILER_CSV = os.path.join(BASE_DIR, "alquiler.csv")
DATABASE_VENTAS = os.path.join(BASE_DIR, "ventas.db")
DATABASE_ALQUILER = os.path.join(BASE_DIR, "alquiler.db")

# Modelos y escaladores (alquiler)
MODELO_LIGHTGBM_ALQUILER = os.path.join(BASE_DIR, "modelo_lgbm_alquiler.pkl")
SCALER_ALQUILER = os.path.join(BASE_DIR, "scaler_alquiler.pkl")
KMEANS_ALQUILER = os.path.join(BASE_DIR, "kmeans_alquiler.pkl")
CLF_DEAL = os.path.join(BASE_DIR, "clf_deal.pkl")
LE_DEAL = os.path.join(BASE_DIR, "le_deal.pkl")
CLF_SEGMENTO_PRECIO = os.path.join(BASE_DIR, "clf_segmento_precio.pkl")
SCALER_SEGMENTO_PRECIO = os.path.join(BASE_DIR, "scaler_segmento_precio.pkl")

# Modelos y escaladores (ventas)
MODELO_LIGHTGBM_VENTAS = os.path.join(BASE_DIR, "modelo_lightgbm_ventas.pkl")
MODELO_TENSORFLOW = os.path.join(BASE_DIR, "modelo_mejorado.keras")
SCALER_VENTAS = os.path.join(BASE_DIR, "scaler_ventas.pkl")
SCALER_TF_X = os.path.join(BASE_DIR, "scaler_X.pkl")
SCALER_TF_Y = os.path.join(BASE_DIR, "scaler_y.pkl")
SCALER_REDES = os.path.join(BASE_DIR, "scaler_redes.pkl")

# GeoJSON para mapas
GEOJSON_DISTRITOS = os.path.join(BASE_DIR, "madrid_distritos.geojson")

# Imágenes y documentos
LOGO_PISOS = os.path.join(BASE_DIR, "pisos_logo.png")
FOTO_PABLO = os.path.join(BASE_DIR, "foto_pablo.jpg")
FOTO_CARLA = os.path.join(BASE_DIR, "foto_carla.png")
FOTO_LUIS = os.path.join(BASE_DIR, "foto_luis.jpg")
FOTO_YONES = os.path.join(BASE_DIR, "foto_yones.jpg")
IMAGEN_PISO = os.path.join(BASE_DIR, "imagen_para_piso.png")
CV_PABLO = os.path.join(BASE_DIR, "Pablo_Iglesias_Lareo.pdf")

# Imágenes de las bases de datos
DATA_BASE_VENTAS = os.path.join(BASE_DIR, "data_base_ventas.png")
DATA_BASE_ALQUILER = os.path.join(BASE_DIR, "data_base_alquiler.png")
