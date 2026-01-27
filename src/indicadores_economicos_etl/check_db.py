import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"), database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), port=os.getenv("DB_PORT")
)
cursor = conn.cursor()

cursor.execute("SELECT * FROM crypto_prices ORDER BY id DESC LIMIT 5;")
rows = cursor.fetchall()

print("\n📊 ULTIMOS 5 DATOS EN LA BASE DE DATOS:")
print("-" * 50)
print(f"{'ID':<5} {'MONEDA':<15} {'PRECIO ($)':<15} {'FECHA'}")
print("-" * 50)
for row in rows:
    print(f"{row[0]:<5} {row[1]:<15} {row[2]:<15} {row[3]}")

conn.close()