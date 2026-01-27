import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def init_db():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()
        
        print("--- INICIALIZANDO BASE DE DATOS (MIGRACIÓN) ---")
        
        # 1. Borramos la tabla vieja si existe (Limpieza)
        print("Eliminando tabla antigua 'cryptos' si existe...")
        cur.execute("DROP TABLE IF EXISTS cryptos;") 
        # También borramos la nueva por si acaso queremos reiniciar
        cur.execute("DROP TABLE IF EXISTS indicadores_economicos;")

        # 2. Creamos la tabla nueva alineada al negocio bancario
        print("Creando tabla nueva 'indicadores_economicos'...")
        cur.execute("""
            CREATE TABLE indicadores_economicos (
                id SERIAL PRIMARY KEY,
                activo VARCHAR(50),  -- Ej: UF, DOLAR
                precio FLOAT,        -- Ej: 36000.50
                fecha DATE,          -- Ej: 2026-01-27
                fuente VARCHAR(100), -- Ej: Banco Central
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Base de datos actualizada exitosamente para Indicadores.")
        
    except Exception as e:
        print(f"❌ Error inicializando DB: {e}")

if __name__ == "__main__":
    init_db()