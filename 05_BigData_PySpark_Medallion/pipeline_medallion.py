# -*- coding: utf-8 -*-
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, round as spark_round, count, sum as spark_sum

# 1. ESTABLECER RUTAS ABSOLUTAS CON VALIDADORES DE SISTEMA
carpeta_base = os.path.dirname(os.path.abspath(__file__))
ruta_bronze = os.path.join(carpeta_base, "data_bronze", "transacciones_raw.csv")

# Asegurar que existan los directorios contenedores para evitar fallos de escritura
os.makedirs(os.path.join(carpeta_base, "data_silver"), exist_ok=True)
os.makedirs(os.path.join(carpeta_base, "data_gold"), exist_ok=True)

ruta_silver_out = os.path.join(carpeta_base, "data_silver", "transacciones_limpias.csv")
ruta_gold_out = os.path.join(carpeta_base, "data_gold", "reporte_kpis.csv")

print(f" Verificando archivo origen en: {ruta_bronze}")

# 2. INICIALIZAR ENTORNO DE PYSPARK CONTROLADO
spark = SparkSession.builder \
    .appName("MedallionArchitecturePipeline") \
    .config("spark.sql.shuffle.partitions", "4") \
    .config("spark.driver.host", "localhost") \
    .getOrCreate()

print(" Motor de PySpark encendido de forma exitosa.")

try:
    if not os.path.exists(ruta_bronze):
        raise FileNotFoundError(f"Falta el archivo transacciones_raw.csv en la capa Bronze.")

    # ==========================================
    #  CAPA BRONZE -> CAPA SILVER (PROCESAMIENTO DE CALIDAD)
    # ==========================================
    print(" Ejecutando transformaciones de limpieza (Capa Bronze -> Silver)...")
    
    # Lectura masiva optimizada
    df_bronze = spark.read.csv(ruta_bronze, header=True, inferSchema=True)
    
    # Reglas de negocio e Ingenieria de Atributos con Spark en memoria
    df_silver = df_bronze \
        .dropDuplicates(["id_transaccion"]) \
        .na.fill({"precio_unitario": 25.0}) \
        .withColumn("fecha_compra", to_timestamp(col("fecha_compra"))) \
        .withColumn("total_venta", spark_round(col("cantidad") * col("precio_unitario"), 2)) \
        .filter(col("cantidad") > 0)
    
    print(" Volcando transformaciones a Capa Silver en disco local...")
    # Pasamos el resultado limpio a un dataframe nativo para evadir el bug de Hadoop en Windows
    df_silver.toPandas().to_csv(ruta_silver_out, index=False, encoding='utf-8')
    print(f" Archivo creado exitosamente en: {ruta_silver_out}")

    # ==========================================
    #  CAPA SILVER -> CAPA GOLD (AGREGACIONES ANALITICAS)
    # ==========================================
    print(" Calculando agregaciones de negocio (Capa Silver -> Gold)...")
    
    # Leemos la capa silver procesada
    df_silver_clean = spark.read.csv(ruta_silver_out, header=True, inferSchema=True)
    
    # Procesamiento analitico pesado
    df_gold_kpis = df_silver_clean.groupBy("pais", "categoria") \
        .agg(
            count("id_transaccion").alias("total_ordenes"),
            spark_round(spark_sum("total_venta"), 2).alias("ingresos_totales"),
            spark_sum("cantidad").alias("unidades_vendidas")
        ) \
        .orderBy(col("ingresos_totales").desc())
    
    print(" Volcando metricas consolidadas a Capa Gold...")
    df_gold_kpis.toPandas().to_csv(ruta_gold_out, index=False, encoding='utf-8')
    print(f" ¡Capa Gold consolidada exitosamente en: {ruta_gold_out}")

    #  Muestra de exito directo en terminal
    print("\n MONITOREO DE KPIs GENERADO EXITOSAMENTE (MUESTRA):")
    df_gold_kpis.show(5)

except Exception as e:
    print(f" Error critico detectado en el flujo: {e}")

finally:
    spark.stop()
    print(" Sesion de PySpark finalizada correctamente.")