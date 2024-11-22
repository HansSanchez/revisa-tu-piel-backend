
# Revisa tu piel - API

<p style="text-align: justify;">
Este proyecto es una aplicación basada en FastAPI que utiliza la API de Google Cloud Vision para la clasificación de imágenes de melanomas y la API de OpenAI para generar sugerencias clínicas basadas en el tipo de melanoma y el porcentaje de riesgos que identificó el modelo de Google.

La aplicación está diseñada para manejar variables de entorno de manera segura y está lista para desplegarse utilizando Docker y Google Cloud Run.
</p>

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

## Características

- **Endpoints para Procesar Datos**: La aplicación incluye un endpoint que genera respuestas basadas en datos de entrada simulados.
- **Integración con OpenAI**: Utiliza la API de OpenAI para generar contenido dinámico.
- **Docker-Ready**: La aplicación está completamente dockerizada para facilitar su despliegue y escalabilidad.
- **Despliegue en Google Cloud Run**: Preparada para un despliegue rápido y seguro en la nube.

## Tecnologías Utilizadas

- FastAPI: Framework web moderno para Python
- Python 3.10: Lenguaje de programación principal
- Google Cloud Vision API: Para la clasificación y caracterización de imágenes
- OpenAI API: Para generación de respuestas inteligentes
- Docker: Para la contenerización de la aplicación
- Google Cloud Run: Para el despliegue en la nube
- Uvicorn: Servidor ASGI para ejecutar la aplicación

## Prerrequisitos

Antes de comenzar, asegúrate de tener lo siguiente instalado en tu máquina:

- Python 3.10 o superior
- Docker y Docker Compose
- Google Cloud SDK (opcional, si planeas desplegar en Google Cloud)
- Git
- Una cuenta en OpenAI para obtener la clave de API
- Una cuenta de Google Cloud Platform con:
  - Google Cloud Vision API habilitada
  - Credenciales de servicio (archivo JSON) con acceso a Cloud Vision API
  - Google Cloud SDK configurado en tu máquina

## Instalación y Configuración

1. **Clona el Repositorio**:
   ```bash
   git clone git@github.com:HansSanchez/revisa-tu-piel-backend.git
   cd revisa-tu-piel-backend
   ```

2. **Crea un Entorno Virtual**:

   **En Windows**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

   **En Unix/Linux**:
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
   GOOGLE_APPLICATION_CREDENTIALS=/ruta/a/tu/archivo/credenciales.json
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
- **Descripción**: Procesa una imagen con un modelo entrenado en Google Cloud Vision y devuelve la categoría y el porcentaje de riesgo.
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

La aplicación puede ser ejecutada usando Docker de dos maneras:

### Método 1: Usando Docker directamente

1. **Construir la Imagen Docker**:
   ```bash
   docker build -t revisa-tu-piel-backend .
   ```

2. **Ejecutar el Contenedor**:
   ```bash
   docker run -d -p 8080:8080      --env-file .env      -v /ruta/local/credenciales.json:/ruta/en/contenedor/credenciales.json      --name revisa-tu-piel      revisa-tu-piel-backend
   ```

   Asegúrate de que en el archivo `.env`, la variable `GOOGLE_APPLICATION_CREDENTIALS` apunta a `/ruta/en/contenedor/credenciales.json`.

3. **Ver logs del contenedor (opcional)**:
   ```bash
   docker logs revisa-tu-piel
   ```

4. **Detener el contenedor**:
   ```bash
   docker stop revisa-tu-piel
   ```

### Método 2: Usando Docker Compose (Recomendado para desarrollo)

1. **Crear archivo docker-compose.yml**:
   ```yaml
   version: '3.8'
   services:
     api:
       build: .
       ports:
         - "8080:8080"
       env_file:
         - .env
       volumes:
         - .:/app
         - /ruta/local/credenciales.json:/ruta/en/contenedor/credenciales.json
       command: uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
   ```

2. **Ejecutar con Docker Compose**:
   ```bash
   docker-compose up -d
   ```

3. **Detener los contenedores**:
   ```bash
   docker-compose down
   ```

### Acceder a la Aplicación

Una vez que los contenedores estén corriendo, puedes acceder a:
- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

### Notas Importantes

- El contenedor expone el puerto 8080.
- Asegúrate de que el archivo `.env` contiene todas las variables de entorno necesarias:
  ```env
  OPENAI_API_KEY=tu-clave-de-api
  GOOGLE_APPLICATION_CREDENTIALS=/ruta/en/contenedor/credenciales.json
  ```
- Si estás usando Google Cloud Vision API, asegúrate de montar el archivo de credenciales correctamente en el contenedor.

## Despliegue en Google Cloud Run

1. **Subir la Imagen a Google Container Registry**:
   ```bash
   gcloud builds submit --tag gcr.io/tu-proyecto/mi-app
   ```

2. **Desplegar en Cloud Run**:
   ```bash
   gcloud run deploy mi-app --image gcr.io/tu-proyecto/mi-app --platform managedZ--region us-central1        --allow-unauthenticated
   ```

## Estructura del Proyecto

```bash
Backend/
├── app/
│   ├── main.py          # Código principal de la aplicación
│   └── __init__.py      # Archivo de inicialización
├── .env                 # Variables de entorno (excluido en .gitignore)
├── .gitignore           # Archivos y directorios ignorados por Git
├── requirements.txt     # Dependencias del proyecto
├── Dockerfile           # Configuración para construir la imagen Docker
└── README.md            # Documento informativo del proyecto
```