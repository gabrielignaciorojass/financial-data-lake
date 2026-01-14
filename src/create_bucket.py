import boto3
import os
from dotenv import load_dotenv

# 1. Cargar las llaves secretas del archivo .env
load_dotenv()

def create_s3_bucket():
    # Recuperamos las variables
    bucket_name = os.getenv("BUCKET_NAME")
    region = os.getenv("AWS_REGION")

    print(f"⏳ Intentando crear el bucket: {bucket_name} en {region}...")

    try:
        # 2. Conectamos con S3 usando boto3
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=region
        )

        # 3. Creamos el bucket
        # Nota: us-east-1 es especial y no requiere especificar LocationConstraint
        if region == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )

        print(f"✅ ¡ÉXITO! Bucket '{bucket_name}' creado correctamente en AWS.")
        print("🚀 Ahora tienes tu Data Lake en la nube.")

    except Exception as e:
        print(f"❌ Error al crear bucket: {e}")

if __name__ == "__main__":
    create_s3_bucket()