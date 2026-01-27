from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Verificar").getOrCreate()

print("--- Leyendo el reporte PARQUET (Sucursales) ---")
# Spark lee la CARPETA completa, no el archivo individual
df_parquet = spark.read.parquet("output/reporte_sucursales")
df_parquet.show()

print("--- Leyendo el reporte CSV (VIPs) ---")
df_csv = spark.read.option("header", "true").csv("output/reporte_vip")
df_csv.show()

spark.stop()