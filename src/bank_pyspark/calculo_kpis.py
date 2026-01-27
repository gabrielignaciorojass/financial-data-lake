from pyspark.sql import SparkSession

# 1. Iniciar Spark
spark = SparkSession.builder \
    .appName("KPIs_Banco_SQL") \
    .getOrCreate()

# 2. Leer el CSV que generamos
# 'header=True' le dice que la primera fila son los nombres de columnas
# 'inferSchema=True' le dice que adivine si el monto es número o texto
df = spark.read.csv("transacciones_banco.csv", header=True, inferSchema=True)

# 3. EL TRUCO DE SQL: Convertimos el DataFrame en una "Vista Temporal"
# Ahora podemos llamarla "transacciones" en nuestras queries
df.createOrReplaceTempView("transacciones")

print("--- Esquema de los datos ---")
df.printSchema()

print("--- Guardando Data Maestra Particionada ---")

# En un Data Lake real, guardamos la data limpia particionada por fecha
# para que sea fácil de consultar en el futuro.
df.write \
    .mode("overwrite") \
    .partitionBy("fecha") \
    .parquet("output/data_lake_partitioned")

print("¡Data Lake actualizado con particiones!")


# 4. KPI 1: ¿Cuánto dinero movió cada sucursal?
kpi_sucursales = spark.sql("""
    SELECT sucursal, count(*) as cantidad, round(sum(monto), 2) as total
    FROM transacciones 
    GROUP BY sucursal
""")

# 5. CARGA (Load): Guardamos el resultado
# mode("overwrite") significa: "Si ya existe la carpeta, bórrala y escribe de nuevo"
print("--- Guardando reporte de Sucursales en formato Parquet ---")
kpi_sucursales.write.mode("overwrite").parquet("output/reporte_sucursales")

# 6. KPI 2: Clientes VIP
kpi_vip = spark.sql("""
    SELECT cliente_id, sum(monto) as total_gastado
    FROM transacciones 
    GROUP BY cliente_id
    HAVING total_gastado > 500000
""")

print("--- Guardando reporte VIP en formato CSV (para Excel) ---")
# A veces Gerencia pide CSV para abrir en Excel, así que guardamos este en CSV
kpi_vip.write.mode("overwrite").option("header", "true").csv("output/reporte_vip")

print("¡Proceso ETL Finalizado con éxito!")
spark.stop()