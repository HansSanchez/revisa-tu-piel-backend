import io
from app.model import predict_with_model_multiple_inputs
import numpy as np
import openai
import os

import tensorflow as tf

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image

load_dotenv()  # Carga las variables del archivo .env
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("La clave OPENAI_API_KEY no está configurada. Verifica tu archivo .env y la configuración de Docker.")

app = FastAPI()

# Crea un cliente de OpenAI
client = openai.Client(
    api_key=api_key
)

def create_prompt(category, percentage):
    prompt = f"""Genera un mensaje breve y empático para el paciente sobre su resultado de melanoma donde:
                {percentage:.2f}% indica riesgo de melanoma {category}.
                Incluye en máximo 4 oraciones:
                1. El resultado directo: "Tu lunar parece ser {category} con {percentage:.2f}% de probabilidad"
                2. Si probabilidad > 60%: ", te recomiendo consultar a un dermatólogo lo antes posible"
                3. Si probabilidad < 60%: ", no te preocupes, tu piel no presenta riesgo alto de melanoma"
                4. Consejo de prevención: ", protege tu piel usando protector solar y evita el sol entre 10am-4pm"
                Usa lenguaje simple, tutea al paciente y mantén un tono tranquilizador pero con un tono directo.
            """
    return prompt

def get_openai_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=550,
            temperature=1
        )
        response_text = response.choices[0].message.content.strip()
        return {response_text}
    except Exception as e:
        print(f"Error al comunicarse con OpenAI: {e}")
        raise HTTPException(status_code=500, detail=f"Error al comunicarse con OpenAI: {e}")
    
def get_highest_prediction(input_data):
    """
    Ejecuta la función predict_with_model_multiple_inputs varias veces y selecciona
    el porcentaje más alto y su categoría correspondiente.

    Args:
        input_data (str): Ruta de entrada a los datos.
        num_iterations (int): Número de iteraciones (entre 5 y 10).

    Returns:
        tuple: Categoría y porcentaje más alto.
    """
    results = []

    for _ in range(3, 11):
        # Generar características aleatorias
        features = np.random.rand(71)
        # Obtener datos del modelo
        category, percentage = predict_with_model_multiple_inputs(input_data, features)
        # Almacenar el resultado
        results.append((category, percentage))

    # Seleccionar el resultado con el porcentaje más alto
    best_result = max(results, key=lambda x: x[1])

    return best_result

@app.post("/process-image/")
def process_image(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen.")
    
    try:
        # Leer el contenido del archivo en memoria
        image_bytes = file.file.read()
        
        # Abrir la imagen usando PIL desde los bytes en memoria
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convertir la imagen a un array de NumPy
        image_array = np.array(image)
        
        # Verifica cómo manejar el tipo de entrada para la función predict_with_model_multiple_inputs
        if hasattr(predict_with_model_multiple_inputs, '__annotations__') and \
            predict_with_model_multiple_inputs.__annotations__.get('image_input') == 'numpy.ndarray':
            # La función espera un array de NumPy
            input_data = image_array
        else:
            # La función espera un objeto con método read (BytesIO)
            image_bytes_io = io.BytesIO()
            image.save(image_bytes_io, format='JPEG')
            image_bytes_io.seek(0)
            input_data = image_bytes_io

        # Obtener datos del modelo
        category, percentage = get_highest_prediction(input_data)
        print(f"Categoría: {category}, Porcentaje: {percentage:.2f}%")

    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen o generar datos. {e}")
    
    try:
        # Crear el prompt
        prompt = create_prompt(category, percentage)
    except Exception as e:
        print(f"Error al crear el prompt: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear el prompt: {e}")
    
    try:
        # Obtener la respuesta de OpenAI
        openai_response = get_openai_response(prompt)
    except Exception as e:
        print(f"Error al obtener la respuesta de OpenAI: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener la respuesta de OpenAI: {e}")
    
    # Retornar los resultados
    return {
        "category": category,
        "percentage": round(percentage, 2),
        "openai_response": openai_response
    }

@app.post("/poc-openai/")
def poc_openai():
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": "Hola cómo estás?"}
            ],
            max_tokens=150,
            temperature=0.7
        )
        response_text = response.choices[0].message.content.strip()
        return {"response": response_text}
    except Exception as e:
        print(f"Error al comunicarse con OpenAI: {e}")
        raise HTTPException(status_code=500, detail=f"Error al comunicarse con OpenAI: {e}")
