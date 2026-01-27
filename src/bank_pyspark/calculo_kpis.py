from pyspark.sql import SparkSession

# 1. Iniciar Spark
spark = SparkSession.builder \
    .appName("KPIs_Banco_SQL") \
    .getOrCreate()

# 2. Leer el CSV con los datos limpios desde Data Lake Silver
print("--- Leyendo datos limpios desde Data Lake Silver ---")
df = spark.read.parquet("output/data_lake_silver_clean")

# 3. Vista Temporal SQL
df.createOrReplaceTempView("transacciones")

print("--- Esquema de los datos ---")
df.printSchema()

# 4. DATA LAKE: Guardado particionado (Zona Silver)
print("--- Guardando Data Maestra Particionada ---")
df.write \
    .mode("overwrite") \
    .partitionBy("fecha") \
    .parquet("output/data_lake_partitioned")
print("¡Data Lake actualizado con particiones!")

# ---------------------------------------------------------
# REGLA DE NEGOCIO 1: EFICIENCIA OPERATIVA
# Objetivo: Medir volumen por sucursal para asignar personal.
# ---------------------------------------------------------
kpi_sucursales = spark.sql("""
    SELECT sucursal, count(*) as cantidad, round(sum(monto), 2) as total
    FROM transacciones 
    GROUP BY sucursal
""")

print("--- Guardando reporte de Sucursales (Parquet) ---")
kpi_sucursales.write.mode("overwrite").parquet("output/reporte_sucursales")

# ---------------------------------------------------------
# REGLA DE NEGOCIO 2: FIDELIZACIÓN (CRÉDITO)
# Objetivo: Detectar clientes con alto "Share of Wallet" (VIPs).
# ---------------------------------------------------------
kpi_vip = spark.sql("""
    SELECT cliente_id, sum(monto) as total_gastado
    FROM transacciones 
    GROUP BY cliente_id
    HAVING total_gastado > 500000
""")

print("--- Guardando reporte VIP (CSV para Gerencia) ---")
kpi_vip.write.mode("overwrite").option("header", "true").csv("output/reporte_vip")

# ---------------------------------------------------------
# REGLA DE NEGOCIO 3: RIESGO Y FRAUDE 
# Objetivo: Alertar transacciones individuales inusualmente grandes.
# ---------------------------------------------------------
kpi_fraude = spark.sql("""
    SELECT *
    FROM transacciones 
    WHERE monto > 200000 
    ORDER BY monto DESC
""")

print("--- Guardando Alerta de Fraude (Parquet para Auditoría) ---")
kpi_fraude.write.mode("overwrite").parquet("output/alerta_fraude")

print("¡Proceso ETL Finalizado con éxito!")
spark.stop()