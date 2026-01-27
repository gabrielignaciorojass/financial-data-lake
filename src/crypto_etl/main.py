import time
from extraction import extract_crypto_data
from datetime import datetime

def start_pipeline():
    """
    Función principal que mantiene el proceso corriendo indefinidamente.
    automatizacion del trabajo
    """
    print("🚀 INICIANDO PIPELINE DE DATOS FINANCIEROS...")
    print("Presiona Ctrl + C para detenerlo en cualquier momento.\n")

    try:
        while True:
            # 1. Obtener la hora actual para el log
            now = datetime.now().strftime("%H:%M:%S")
            print(f"[{now}] ⏰ Ejecutando tarea programada...")
            
            # 2. Ejecutar la extracción 
            extract_crypto_data()
            
            # 3. Esperar antes de la siguiente ejecución
            # Para pruebas, pongamos 60 segundos (1 minuto)
            # En producción real, esto podría ser 3600 (1 hora)
            segundos_espera = 60
            print(f"💤 Esperando {segundos_espera} segundos para la siguiente vuelta...\n")
            time.sleep(segundos_espera)

    except KeyboardInterrupt:
        # Esto permite parar el código limpiamente con Ctrl + C
        print("\n🛑 Pipeline detenido por el usuario.")

if __name__ == "__main__":
    start_pipeline()