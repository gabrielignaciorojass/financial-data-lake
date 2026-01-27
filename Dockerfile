# 1. Usar una imagen base de Python oficial (ligera)
FROM python:3.9-slim

# ------------------------
# Instalación de Java (requerido para PySpark)
# Usamos 'default-jre' para evitar errores de versión específica
RUN apt-get update && \
    apt-get install -y default-jre && \
    apt-get clean;

ENV JAVA_HOME=/usr/lib/jvm/default-java
# ------------------------

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar el archivo de requerimientos e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar todo el código del proyecto al contenedor

COPY . .

# CMD actualizado a la nueva ruta
CMD ["sh", "-c", "python src/bank_pyspark/generar_datos.py && python src/bank_pyspark/calculo_kpis.py"]