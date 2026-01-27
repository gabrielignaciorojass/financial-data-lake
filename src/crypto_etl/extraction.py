import requests
import json
import boto3
import os
from datetime import datetime
from dotenv import load_dotenv

# 1. Cargar credenciales del archivo .env
load_dotenv()

# Configuración
BUCKET_NAME = os.getenv("BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")

def upload_to_s3(data, filename):
    """
    Sube el archivo JSON directamente al Bucket S3 en AWS.
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=AWS_REGION
    )

    try:
        # Convertimos el diccionario Python a texto JSON
        json_string = json.dumps(data, indent=4)
        
        # Definimos la "key" (ruta dentro del bucket). 
        # Organizamos por fecha para mantener orden: raw/2026-01-13/archivo.json
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        s3_key = f"raw/{fecha_hoy}/{filename}"

        print(f"☁️ Subiendo a S3: {BUCKET_NAME}/{s3_key} ...")
        
        # Subimos el objeto
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=json_string,
            ContentType='application/json'
        )
        print("✅ ¡Archivo subido exitosamente a la nube!")
        return True

    except Exception as e:
        print(f"❌ Error al subir a S3: {e}")
        return False

def extract_crypto_data():
    """
    Función principal: Extrae -> Sube a S3
    """
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,tether,solana",
        "vs_currencies": "usd",
        "include_last_updated_at": "true"
    }
    
    print("⏳ Consultando API de CoinGecko...")
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("📦 Datos recibidos correctamente.")
            
            # Generamos nombre único
            timestamp = datetime.now().strftime("%H-%M-%S")
            filename = f"prices_{timestamp}.json"
            
            # En lugar de guardar en disco local, enviamos a AWS
            upload_to_s3(data, filename)
            
        else:
            print(f"❌ Error API: {response.status_code}")

    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    extract_crypto_data()