import psycopg2
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def init_database():
    print("⏳ Conectando a la Base de Datos en AWS RDS...")
    try:
        # 1. Establecer conexión
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        conn.autocommit = True # Para que los cambios se guarden automáticamente
        cursor = conn.cursor()
        
        print("✅ Conexión exitosa. Leyendo esquema SQL...")

        # 2. Leer el archivo SQL
        with open('sql/schema.sql', 'r') as file:
            sql_script = file.read()

        # 3. Ejecutar el SQL
        cursor.execute(sql_script)
        print("🚀 ¡Tabla 'crypto_prices' creada exitosamente en la nube!")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error al conectar o crear tabla: {e}")
        print("💡 Si es un timeout, revisa el 'Security Group' en AWS.")

if __name__ == "__main__":
    init_database()