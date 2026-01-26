# 1. Usar una imagen base de Python oficial (ligera)
FROM python:3.9-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar el archivo de requerimientos e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar todo el código del proyecto al contenedor
COPY src/ ./src/
# Copiamos el .env también (OJO: En producción real esto se hace diferente por seguridad, 
# pero para aprender ahora está bien pasar el archivo).
COPY .env .

# 5. Comando por defecto al iniciar el contenedor
# Por ahora, haremos que corra la extracción y carga
CMD ["sh", "-c", "python src/extraction.py && python src/load_data.py"]