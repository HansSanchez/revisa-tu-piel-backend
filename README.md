# FastAPI OpenAI API Integration

Este proyecto es una aplicación basada en FastAPI que utiliza la API de OpenAI para generar respuestas basadas en entradas específicas. La aplicación está diseñada para manejar variables de entorno de manera segura y está lista para desplegarse utilizando Docker y Google Cloud Run.

## Tabla de Contenidos

- [Características](#características)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Prerrequisitos](#prerrequisitos)
- [Instalación y Configuración](#instalación-y-configuración)
- [Ejecutar la Aplicación](#ejecutar-la-aplicación)
- [Uso](#uso)
- [Dockerización](#dockerización)
- [Despliegue en Google Cloud Run](#despliegue-en-google-cloud-run)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

## Características

- **Endpoints para Procesar Datos**: La aplicación incluye un endpoint que genera respuestas basadas en datos de entrada simulados.
- **Integración con OpenAI**: Utiliza la API de OpenAI para generar contenido dinámico.
- **Docker-Ready**: La aplicación está completamente dockerizada para facilitar su despliegue y escalabilidad.
- **Despliegue en Google Cloud Run**: Preparada para un despliegue rápido y seguro en la nube.

## Tecnologías Utilizadas

- FastAPI: Framework web moderno para Python
- Python 3.10: Lenguaje de programación principal
- OpenAI API: Para generación de respuestas inteligentes
- Docker: Para la contenedorización de la aplicación
- Google Cloud Run: Para el despliegue en la nube
- Uvicorn: Servidor ASGI para ejecutar la aplicación

## Prerrequisitos

Antes de comenzar, asegúrate de tener lo siguiente instalado en tu máquina:

- Python 3.10 o superior
- Docker y Docker Compose
- Google Cloud SDK (opcional, si planeas desplegar en Google Cloud)
- Una cuenta en OpenAI para obtener la clave de API

## Instalación y Configuración

1. **Clona el Repositorio**:
```bash
git clone https://github.com/tu-usuario/fastapi-openai-integration.git
cd fastapi-openai-integration
```

2. **Crea un Entorno Virtual**:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Instala las Dependencias**:
```bash
pip install -r requirements.txt
```

4. **Configura las Variables de Entorno**:

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
```env
OPENAI_API_KEY=tu-clave-de-api
```

## Ejecutar la Aplicación

1. **Ejecutar en Desarrollo**:
```bash
uvicorn app.main:app --reload
```

2. **Acceder a la Aplicación**:
- Documentación interactiva (Swagger UI): http://127.0.0.1:8000/docs
- Documentación alternativa (ReDoc): http://127.0.0.1:8000/redoc

## Uso

### Endpoints Disponibles

#### POST /process-image/
- **Descripción**: Procesa una imagen (simulada) y genera respuestas basadas en datos aleatorios.
- **Parámetros**: 
  - `file`: Archivo de imagen

**Respuesta de Ejemplo**:
```json
{
  "category": "Melanocítico",
  "percentage": 73.5,
  "openai_response": "Recomendación médica basada en la categoría Melanocítico."
}
```

#### POST /poc-openai/
- **Descripción**: Realiza una prueba de concepto enviando un mensaje a la API de OpenAI.

**Respuesta de Ejemplo**:
```json
{
  "response": "Hola, esto es un ejemplo de respuesta desde OpenAI."
}
```

## Dockerización

1. **Construir la Imagen Docker**:
```bash
docker build -t mi-app-fastapi .
```

2. **Ejecutar el Contenedor**:
```bash
docker run -d -p 8000:8000 --env-file .env mi-app-fastapi
```

3. **Acceder a la Aplicación**:
- Swagger UI: http://localhost:8000/docs

## Despliegue en Google Cloud Run

1. **Subir la Imagen a Google Container Registry**:
```bash
gcloud builds submit --tag gcr.io/tu-proyecto/mi-app
```

2. **Desplegar en Cloud Run**:
```bash
gcloud run deploy mi-app \
    --image gcr.io/tu-proyecto/mi-app \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

## Estructura del Proyecto

```bash
Backend/
├── app/
│   ├── main.py          # Código principal de la aplicación
│   └── __init__.py      # Archivo de inicialización
├── .env                 # Variables de entorno (excluido en .gitignore)
├── .gitignore          # Archivos y directorios ignorados por Git
├── requirements.txt     # Dependencias del proyecto
└── Dockerfile          # Configuración para construir la imagen Docker
```

## Contribuir

Si deseas contribuir a este proyecto, sigue estos pasos:

1. Haz un fork del repositorio
2. Crea una rama con tu función/corrección (`git checkout -b mi-nueva-funcion`)
3. Realiza tus cambios y haz commit (`git commit -m 'Agregada nueva función'`)
4. Envía tus cambios a tu fork (`git push origin mi-nueva-funcion`)
5. Abre un Pull Request en el repositorio principal

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.
