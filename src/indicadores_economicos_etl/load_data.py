import os
import psycopg2
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

def load_to_sql(df):
    """
    Toma el DataFrame de Indicadores Económicos (UF, Dólar) 
    y lo inserta en AWS RDS (PostgreSQL).
    """
    if df.empty:
        print("⚠️ No hay datos para cargar.")
        return

    print("🔌 Conectando a Base de Datos AWS RDS...")
    conn = None
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"), # Asegúrate que esto coincida con tu .env
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor()
        
        query = """
            INSERT INTO indicadores_economicos (activo, precio, fecha, fuente)
            VALUES (%s, %s, %s, %s);
        """
        
        print(f"📥 Insertando {len(df)} registros de indicadores...")

        for index, row in df.iterrows():
            cursor.execute(query, (
                row['activo'], 
                row['precio'], 
                row['fecha'], 
                row['fuente']
            ))
        
        conn.commit()
        print("✅ ¡Carga exitosa a la Nube! Los indicadores están actualizados.")
        
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error crítico en Base de Datos: {e}")
        if conn:
            conn.close()