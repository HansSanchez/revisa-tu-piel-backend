# Utiliza una imagen base de Python 3.10
FROM python:3.10-slim

# Configura el directorio de trabajo dentro del contenedor
WORKDIR /app

# Actualiza pip a la última versión
RUN python3 -m pip install --upgrade pip

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación al contenedor
COPY . .

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 8080

# Comando para ejecutar la aplicación usando uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
