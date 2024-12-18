import io
from app.model import predict_with_model_multiple_inputs
import numpy as np
import openai
import os

import tensorflow as tf

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

load_dotenv()  # Carga las variables del archivo .env
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("La clave OPENAI_API_KEY no está configurada. Verifica tu archivo .env y la configuración de Docker.")

app = FastAPI()

# Lista única de orígenes permitidos
origins = [
    "http://localhost:5173",  # Desarrollo local
    "http://127.0.0.1:5173",  # Desarrollo local
    "http://45.189.119.147",  # Acceso IP pública
    "http://172.16.100.147",  # Acceso IP privada
    "https://melanomia.minciencias.gov.co"  # Producción
]

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Lista única de orígenes
    allow_credentials=False,  # Habilitado para cookies o autenticación
    allow_methods=["POST"],  # Métodos permitidos
    allow_headers=["*"],  # Permitir todos los encabezados
)
print("Configuración de CORS completada.")

# Crea un cliente de OpenAI
client = openai.Client(
    api_key=api_key
)

def create_prompt(category, percentage):
    prompt = f"""A partir del riesgo ({category}) y la probabilidad de que el lunar observado ({percentage}%), generar un mensaje concreto y claro en tono amigable al paciente, con la siguiente estructura.

                1. Comunicar al paciente el resultado obtenido del análisis de la fotografía.
                2. Indicar al paciente la necesidad de acudir a un medico o dermatólogo según el riesgo obtenido, si es alto incitarlo a ir de manera urgente.
                3. Generar dos recomendaciones sencillas sobre el cuidado de la piel y la exposición prolongada a la radiación UV.
                4. Indicar al paciente signos de alarma.
                5. Tutear al paciente.
                6. Incluir el valor de la probabilidad en caso de que el riesgo sea alto o moderado.
                7. Limitar el mensaje a 150 palabras.
            """
    return prompt

def get_openai_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-2024-11-20",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
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

    for _ in range(3, 5):
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
    # Validar que el archivo sea una imagen
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen.")
    
    try:
        # Leer el contenido del archivo en memoria
        image_bytes = file.file.read()
        
        # Abrir la imagen usando PIL desde los bytes en memoria
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convertir la imagen al modo RGB si es necesario
        if image.mode == "RGBA":
            image = image.convert("RGB")
        elif image.mode != "RGB":
            # Asegurar que esté en un formato compatible
            raise HTTPException(status_code=400, detail="El formato de la imagen no es compatible.")

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
        prompt = create_prompt(category, round(percentage, 2))
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
            model="gpt-4o-2024-11-20",
            messages=[
                {"role": "user", "content": "Hola cómo estás?"}
            ],
            max_tokens=150,
            temperature=1
        )
        response_text = response.choices[0].message.content.strip()
        return {"response": response_text}
    except Exception as e:
        print(f"Error al comunicarse con OpenAI: {e}")
        raise HTTPException(status_code=500, detail=f"Error al comunicarse con OpenAI: {e}")
