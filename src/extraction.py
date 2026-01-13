import requests  # Librería para "hablar" con internet y hacer peticiones HTTP
import json      # Librería para manejar el formato de datos que nos devuelve la API

def extract_crypto_data():
    """
    Función encargada de ir a buscar los precios actuales de Bitcoin y Ethereum.
    Retorna: Un diccionario con los datos o None si falla.
    """
    
    # 1. Definimos la dirección (URL) de la API de CoinGecko
    url = "https://api.coingecko.com/api/v3/simple/price"
    
    # 2. Definimos los parámetros (¿Qué queremos pedir exactamente?)
    # ids: Las monedas que queremos (bitcoin y ethereum)
    # vs_currencies: En qué moneda queremos el precio (dólares 'usd')
    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "usd"
    }
    
    print("⏳ Conectando con la API de CoinGecko...")
    
    try:
        # 3. Hacemos la petición GET (como si escribieras la URL en el navegador)
        response = requests.get(url, params=params, timeout=10)
        
        # 4. Verificamos si la respuesta fue exitosa 
        if response.status_code == 200:
            data = response.json() # Convertimos la respuesta a formato utilizable por Python
            print("✅ ¡Éxito! Datos recibidos:")
            print(json.dumps(data, indent=4)) # Imprimimos bonito para leerlo
            return data
        else:
            # Si no es 200, algo salió mal (ej: error 404 o 500)
            print(f"❌ Error en la API. Código de estado: {response.status_code}")
            return None

    except Exception as e:
        # Capturamos errores de conexión (ej: no tienes internet)
        print(f"❌ Error crítico de conexión: {e}")
        return None

# Bloque principal: Esto solo se ejecuta si corremos este archivo directamente
if __name__ == "__main__":
    extract_crypto_data()