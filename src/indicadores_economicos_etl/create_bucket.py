import boto3
import os
from dotenv import load_dotenv

# Cargar variables de entorno (.env)
load_dotenv()

def create_bucket():
    """
    Crea un S3 Bucket en AWS usando las credenciales del archivo .env
    """
    bucket_name = os.getenv("BUCKET_NAME")
    region = os.getenv("AWS_REGION")

    # Validación básica
    if not bucket_name:
        print("❌ Error: No se encontró la variable BUCKET_NAME en el archivo .env")
        return

    print(f"--- Intentando crear bucket: {bucket_name} ---")

    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=region
        )

        # Lógica para crear el bucket
        # Nota: us-east-1 es especial y no requiere 'LocationConstraint'
        if region == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )

        print(f"✅ ¡Éxito! El bucket '{bucket_name}' está listo en AWS.")

    except Exception as e:
        # Si falla, imprimimos por qué (puede ser que ya exista, credenciales malas, etc.)
        print(f"⚠️ Aviso o Error: {e}")

if __name__ == "__main__":
    create_bucket()