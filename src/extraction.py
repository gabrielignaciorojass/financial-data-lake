import requests
import json
import os
from datetime import datetime

# CONFIGURACIÓN
# Definimos dónde queremos guardar los archivos (ruta relativa)
DATA_PATH = "data/raw"

def save_raw_data(data):
    """
    Función para guardar los datos en un archivo JSON local.
    Simula el guardado en un Data Lake (S3).
    """
    # 1. Aseguramos que la carpeta exista. Si no, la crea.
    os.makedirs(DATA_PATH, exist_ok=True)
    
    # 2. Generamos un nombre único usando la fecha y hora actual
    # Ejemplo: crypto_2026-01-13_15-30-00.json
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"crypto_{timestamp}.json"
    full_path = os.path.join(DATA_PATH, filename)
    
    # 3. Guardamos el archivo
    try:
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"💾 Archivo guardado exitosamente en: {full_path}")
    except Exception as e:
        print(f"❌ Error al guardar archivo: {e}")

def extract_crypto_data():
    """
    Función principal de extracción.
    """
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,tether",
        "vs_currencies": "usd",
        "include_last_updated_at": "true" # Pedimos también la fecha de actualización
    }
    
    print("⏳ Consultando API...")
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Datos recibidos. Guardando...")
            
            # LLAMAMOS A LA NUEVA FUNCIÓN DE GUARDADO
            save_raw_data(data)
            
        else:
            print(f"❌ Error API: {response.status_code}")

    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    extract_crypto_data()