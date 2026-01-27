import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Configuración: Evitamos que cree archivos temporales basura (__pycache__)
sys.dont_write_bytecode = True

def iniciar_sesion_spark():
    """Inicia una sesión de Spark solo para lectura."""
    return SparkSession.builder \
        .appName("Auditor_Data_Lake") \
        .master("local[*]") \
        .getOrCreate()

def auditar_calidad_datos():
    spark = iniciar_sesion_spark()
    print("\n" + "="*50)
    print("🕵️‍♂️  INICIANDO AUDITORÍA DEL DATA LAKE")
    print("="*50)

    # RUTA A INSPECCIONAR (La Capa Silver Limpia)
    # Nota: Usamos ruta relativa asumiendo que el script corre desde la raíz
    ruta_silver = "output/data_lake_silver_clean"

    # 1. VERIFICACIÓN DE EXISTENCIA
    if not os.path.exists(ruta_silver):
        print(f"❌ ERROR CRÍTICO: No se encuentra la carpeta: {ruta_silver}")
        print("   ¿Ejecutaste el pipeline de limpieza antes?")
        return

    try:
        df = spark.read.parquet(ruta_silver)
        print(f"✅ CONEXIÓN EXITOSA: Se pudo leer el formato Parquet.")
    except Exception as e:
        print(f"❌ ERROR DE FORMATO: Los archivos están corruptos. {e}")
        return

    # 2. AUDITORÍA DE VOLUMEN
    total_registros = df.count()
    print(f"📊 VOLUMEN: Se encontraron {total_registros} transacciones procesadas.")

    if total_registros == 0:
        print("⚠️  ALERTA: El Data Lake está vacío.")
    
    # 3. AUDITORÍA DE CALIDAD (Busca si escapó basura)
    # Buscamos nulos en 'monto' o 'cliente_id'
    errores = df.filter(col("monto").isNull() | col("cliente_id").isNull()).count()

    if errores == 0:
        print("✅ CALIDAD APROBADA: 0 registros nulos encontrados.")
        print("   El filtro de limpieza funcionó correctamente.")
    else:
        print(f"❌ FALLO DE CALIDAD: Se encontraron {errores} registros sucios.")

    # 4. MUESTRA 
    print("\n--- 🔍 EVIDENCIA (Muestra Aleatoria) ---")
    df.select("fecha", "tipo", "monto", "sucursal").show(5, truncate=False)

    print("="*50)
    print("🏁 FIN DE LA AUDITORÍA")
    print("="*50)
    spark.stop()

if __name__ == "__main__":
    auditar_calidad_datos()