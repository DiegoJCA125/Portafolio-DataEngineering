# -*- coding: utf-8 -*-
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, round as spark_round, count, sum as spark_sum

# 1. OBTENER RUTAS ABSOLUTAS
carpeta_base = os.path.dirname(os.path.abspath(__file__))
ruta_bronze = os.path.join(carpeta_base, "data_bronze", "transacciones_raw.csv")
ruta_silver = os.path.join(carpeta_base, "data_silver", "datos_limpios")
ruta_gold = os.path.join(carpeta_base, "data_gold", "reporte_kpis")

print(f"📂 Buscando archivo Bronze en: {ruta_bronze}")

# 2. INICIALIZAR LA SESION DE SPARK CON CONFIGURACION DE EVASION PARA WINDOWS
spark = SparkSession.builder \
    .appName("MedallionArchitecturePipeline") \
    .config("spark.sql.shuffle.partitions", "5") \
    .config("spark.driver.host", "localhost") \
    .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.RawLocalFileSystem") \
    .getOrCreate()

print("🚀 Sesion de PySpark inicializada con exito.")

try:
    if not os.path.exists(ruta_bronze):
        raise FileNotFoundError(f"No se encontro el archivo base en {ruta_bronze}.")

    # ==========================================
    # 🔥 CAPA BRONZE -> CAPA SILVER (LIMPIEZA)
    # ==========================================
    print("⏳ Procesando Capa Bronze -> Capa Silver...")
    
    # Leer datos crudos de Bronze
    df_bronze = spark.read.csv(ruta_bronze, header=True, inferSchema=True)
    
    # Limpieza de calidad de datos
    df_silver = df_bronze \
        .dropDuplicates(["id_transaccion"]) \
        .na.fill({"precio_unitario": 25.0}) \
        .withColumn("fecha_compra", to_timestamp(col("fecha_compra"))) \
        .withColumn("total_venta", spark_round(col("cantidad") * col("precio_unitario"), 2)) \
        .filter(col("cantidad") > 0)
    
    print("💾 Escribiendo datos limpios en data_silver (Formato optimizado para Windows)...")
    # Coalesce evita que cree multiples fragmentos y previene el error de permisos
    df_silver.coalesce(1).write.mode("overwrite").csv(ruta_silver, header=True)
    print("✨ Capa Silver guardada exitosamente.")

    # ==========================================
    # 🏆 CAPA SILVER -> CAPA GOLD (AGREGACIONES)
    # ==========================================
    print("⏳ Procesando Capa Silver -> Capa Gold...")
    
    # Leer datos limpios desde Silver
    df_silver_clean = spark.read.csv(ruta_silver, header=True, inferSchema=True)
    
    # Calcular KPIs del negocio
    df_gold_kpis = df_silver_clean.groupBy("pais", "categoria") \
        .agg(
            count("id_transaccion").alias("total_ordenes"),
            spark_round(spark_sum("total_venta"), 2).alias("ingresos_totales"),
            spark_sum("cantidad").alias("unidades_vendidas")
        ) \
        .orderBy(col("ingresos_totales").desc())
    
    print("💾 Escribiendo reporte final en data_gold...")
    df_gold_kpis.coalesce(1).write.mode("overwrite").csv(ruta_gold, header=True)
    print("🏆 ¡Capa Gold consolidada con éxito!")

    # Mostrar reporte en consola para verificar exito
    print("\n📊 MUESTRA DEL REPORTE ANALITICO FINAL (CAPA GOLD):")
    df_gold_kpis.show(10)

except Exception as e:
    print(f"❌ Error en la ejecucion del pipeline de Spark: {e}")

finally:
    spark.stop()
    print("🛑 Sesion de PySpark finalizada correctamente.")