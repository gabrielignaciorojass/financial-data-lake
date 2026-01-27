import requests
import pandas as pd
from datetime import datetime

def extract_financial_data():
    """
    Conecta a la API de mindicador.cl para obtener los indicadores económicos
    críticos para la operación bancaria chilena (UF, Dólar, Euro).
    """
    url = "https://mindicador.cl/api"
    
    print(f"--- INICIO ETL DE MERCADO ---")
    print(f"Conectando a fuente oficial: {url} ...")
    
    try:
        response = requests.get(url)
        response.raise_for_status() # Lanza error si la web está caída
        data = response.json()
        
        # Extraemos solo lo que le importa al Banco 
        # La API devuelve objetos con 'codigo', 'nombre', 'valor', 'fecha'
        indicadores = [
            {
                "activo": "UF",
                "precio": data['uf']['valor'],
                "fecha": str(datetime.now().date()),
                "fuente": "Banco Central / Mindicador"
            },
            {
                "activo": "DOLAR", # Dólar Observado
                "precio": data['dolar']['valor'],
                "fecha": str(datetime.now().date()),
                "fuente": "Bolsa Electrónica"
            },
            {
                "activo": "EURO",
                "precio": data['euro']['valor'],
                "fecha": str(datetime.now().date()),
                "fuente": "Banco Central"
            },
            {
                "activo": "UTM",
                "precio": data['utm']['valor'],
                "fecha": str(datetime.now().date()),
                "fuente": "Tesorería General"
            }
        ]
        
        # Convertimos a DataFrame para visualizar fácil
        df = pd.DataFrame(indicadores)
        print("✅ Extracción exitosa de Indicadores Económicos:")
        print(df)
        
        return df
        
    except Exception as e:
        print(f"❌ Error crítico obteniendo indicadores: {e}")
        return pd.DataFrame() # Retorna vacío si falla

if __name__ == "__main__":
    extract_financial_data()