from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import random
import openai
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI()

# Crea un cliente de OpenAI
client = openai.Client(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_random_data():
    categories = ["Melanocítico", "Displásico", "Congénito", "Azul", "Halo", "Spitz", "Nevus de Reed"]
    random_category = random.choice(categories)
    random_percentage = round(random.uniform(0, 100), 2)
    return random_category, random_percentage

def create_prompt(category, percentage):
    prompt = f"Eres un experto en medicina y tu tarea es proporcionar una sugerencia médica para un lunar de tipo '{category}' con un porcentaje de riesgo de {percentage}%."
    return prompt

def get_openai_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
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

@app.post("/process-image/")
def process_image(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen.")

    try:
        # Generar datos aleatorios
        category, percentage = generate_random_data()
        print(f"Datos aleatorios generados: {category}, {percentage}")
    except Exception as e:
        print(f"Error al generar datos aleatorios: {e}")

    try:
        # Crear el prompt
        prompt = create_prompt(category, percentage)
        print(f"Prompt creado: {prompt}")
    except Exception as e:
        print(f"Error al crear el prompt: {e}")

    try:
        # Obtener la respuesta de OpenAI
        openai_response = get_openai_response(prompt)
        print(f"Respuesta de OpenAI obtenida: {openai_response}")
    except Exception as e:
        print(f"Error al obtener la respuesta de OpenAI: {e}")

    # Retornar los resultados
    return {
        "category": category,
        "percentage": percentage,
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
