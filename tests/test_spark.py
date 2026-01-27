from pyspark.sql import SparkSession

# 1. Iniciar la sesión de Spark (Esto reemplaza a abrir un Excel)
spark = SparkSession.builder \
    .appName("PruebaFinancialETL") \
    .master("local[*]") \
    .getOrCreate()

print("¡Spark se inició correctamente!")

# 2. Crear un DataFrame de prueba pequeño
data = [("Bitcoin", 45000), ("Ethereum", 3000), ("Solana", 100)]
columns = ["Cripto", "Precio"]

df = spark.createDataFrame(data, columns)

# 3. Mostrar los datos (Equivalente a print(df.head()) en Pandas)
df.show()

# 4. Detener la sesión
spark.stop()