import streamlit as st
import tensorflow as tf
import pickle

@st.cache_resource
def load_model_and_scaler():
    model = tf.keras.models.load_model("modelo_mejorado.keras")
    
    with open("scaler_X.pkl", "rb") as f:
        scaler_X = pickle.load(f)
    with open("scaler_y.pkl", "rb") as f:
        scaler_y = pickle.load(f)
    
    return model, scaler_X, scaler_y

