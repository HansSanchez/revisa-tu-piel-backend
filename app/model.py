import numpy as np
import os
import gdown
import pandas as pd
from PIL import Image
from tensorflow.keras.models import load_model
import tempfile

# URL del archivo en Google Drive
drive_file_id = "1DebLQ8PFZtUBSJnwMhr1WcfC_wQhSRWs"
drive_url = f"https://drive.google.com/uc?id={drive_file_id}"

def download_model_temporarily(drive_url):
    """
    Descarga un modelo desde Google Drive y lo almacena temporalmente.

    Args:
        drive_url (str): Enlace directo al archivo en Google Drive.

    Returns:
        str: Ruta temporal al archivo descargado.
    """
    print("Descargando modelo desde Google Drive...")
    temp_dir = tempfile.gettempdir()
    model_temp_path = os.path.join(temp_dir, "MODELO_01.keras")
    gdown.download(drive_url, model_temp_path, quiet=False)
    print("Descarga completada. Usando modelo en memoria temporal.")
    return model_temp_path

# Descargar y cargar el modelo desde una ruta temporal
model_path = download_model_temporarily(drive_url)
model = load_model(model_path)

def preprocess_image(image_path, target_size=(128, 128)):
    """
    Carga y procesa una imagen para usar con un modelo Keras.

    Args:
        image_path (str): Ruta a la imagen.
        target_size (tuple): Dimensiones a las que se redimensionará la imagen.

    Returns:
        numpy.ndarray: Imagen procesada y lista para el modelo.
    """
    # Cargar la imagen
    img = Image.open(image_path).convert("RGB")
    # Redimensionar la imagen
    img = img.resize(target_size)
    # Convertir a array y escalar los valores de píxel
    img_array = np.array(img) / 255.0
    # Agregar dimensión para lotes
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_with_model_multiple_inputs(image_path, features):
    """
    Realiza una predicción con un modelo Keras usando múltiples entradas.

    Args:
        image_path (str): Ruta a la imagen a usar para la predicción.
        features (numpy.ndarray): Entrada adicional requerida por el modelo.

    Returns:
        tuple: Categoría predicha ("Maligno" o "Benigno") y porcentaje de certeza.
    """
    processed_image = preprocess_image(image_path)
    # Asegurarse de que las características tengan la forma correcta
    features = np.expand_dims(features, axis=0)  # Convertir a batch
    # Crear el diccionario de entradas
    inputs = {"images": processed_image, "features": features}
    # Realizar la predicción
    prediction = model.predict(inputs)
    
    # Convertimos a porcentaje
    percent = prediction * 100.0
    
    if (percent > 0.0 and percent <= 20.0):
        category = "Bajo riesgo"
    elif percent > 20.0 and percent < 60.0:
        category = "Riesgo moderado"
    elif percent >= 60.0 and percent <= 100.0:
        category = "Alto riesgo"
    else:
        category = "No se pudo determinar la categoría"
        
    return category, percent.item()
