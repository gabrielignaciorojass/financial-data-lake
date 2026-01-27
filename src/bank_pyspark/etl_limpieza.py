from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("LimpiezaDatos").getOrCreate()

print("--- 1. INGESTA: Leyendo datos crudos ---")
# Leemos el CSV sucio
df_raw = spark.read.csv("transacciones_banco.csv", header=True, inferSchema=True)

# Contamos cuántos datos llegaron
total_inicial = df_raw.count()
print(f"Total de registros recibidos: {total_inicial}")

# Mostramos un poco de la basura (filas con nulls)
print("--- Muestra de datos sucios (Nulos) ---")
df_raw.filter(col("monto").isNull()).show(5)

print("--- 2. TRANSFORMACIÓN: Aplicando Reglas de Calidad ---")

# REGLA 1: Eliminar filas donde el monto sea Nulo
# (No podemos inventar dinero, así que descartamos esas transacciones corruptas)
df_sin_nulos = df_raw.dropna(subset=["monto"])

# REGLA 2: Eliminar transacciones duplicadas
# (Si el ID, cliente, monto y fecha son iguales, es un duplicado)
df_limpio = df_sin_nulos.dropDuplicates(["id_transaccion", "cliente_id", "monto", "fecha"])

# Contamos cuánto quedó
total_final = df_limpio.count()
basura_eliminada = total_inicial - total_final

print(f"--- REPORTE DE CALIDAD ---")
print(f"Registros iniciales: {total_inicial}")
print(f"Registros finales:   {total_final}")
print(f"Data eliminada:    {basura_eliminada} filas ({(basura_eliminada/total_inicial)*100:.1f}%)")

print("--- 3. CARGA: Guardando en Capa Silver (Partitioned) ---")
# Guardamos la data limpia, lista para que el script de KPIs la use
df_limpio.write \
    .mode("overwrite") \
    .partitionBy("fecha") \
    .parquet("output/data_lake_silver_clean")

print("¡Limpieza completada! Datos guardados en 'output/data_lake_silver_clean'")
spark.stop()