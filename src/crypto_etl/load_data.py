import boto3
import json
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración
BUCKET_NAME = os.getenv("BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")

# Conexión a S3
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=AWS_REGION
)

def get_latest_file_from_s3():
    """
    Busca el archivo más reciente en la carpeta 'raw/' del bucket.
    """
    print("🔎 Buscando el archivo más reciente en S3...")
    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix='raw/')
        if 'Contents' not in response:
            print("⚠️ El bucket está vacío o no hay carpeta raw/")
            return None

        # Ordenamos los archivos por fecha (el último al final)
        files = sorted(response['Contents'], key=lambda x: x['LastModified'])
        latest_file = files[-1] # El último de la lista
        
        key = latest_file['Key']
        print(f"📄 Archivo encontrado: {key}")
        
        # Descargamos el contenido del archivo (sin guardarlo en disco)
        obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=key)
        content = obj['Body'].read().decode('utf-8')
        return json.loads(content)
        
    except Exception as e:
        print(f"❌ Error leyendo S3: {e}")
        return None

def insert_data_to_rds(data):
    """
    Toma el JSON y lo inserta en PostgreSQL.
    """
    if not data:
        return

    print("🔌 Conectando a Base de Datos...")
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor()
        
        # El JSON viene así: {'bitcoin': {'usd': 95000, ...}, 'ethereum': ...}
        # Vamos a recorrer cada moneda
        for coin, details in data.items():
            price = details['usd']
            # Convertimos el timestamp de UNIX a fecha normal si viene, si no, usa el de la DB
            
            query = """
                INSERT INTO crypto_prices (symbol, price_usd)
                VALUES (%s, %s);
            """
            cursor.execute(query, (coin, price))
        
        conn.commit() # ¡Guardar cambios!
        print(f"✅ ¡{len(data)} registros insertados correctamente en la Nube!")
        
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error de Base de Datos: {e}")

if __name__ == "__main__":
    # 1. Obtener datos de S3
    json_data = get_latest_file_from_s3()
    
    # 2. Guardar en RDS
    if json_data:
        insert_data_to_rds(json_data)