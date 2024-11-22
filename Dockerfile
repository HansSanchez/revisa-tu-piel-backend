# Usa una imagen base de Python ligera
FROM python:3.11-slim

# Configura el directorio de trabajo dentro del contenedor
WORKDIR /app

# Actualiza e instala dependencias del sistema si es necesario
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Actualiza pip antes de instalar dependencias
RUN pip install --no-cache-dir --upgrade pip

# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación al contenedor
COPY . .

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 8080

# Comando para ejecutar la aplicación usando uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
