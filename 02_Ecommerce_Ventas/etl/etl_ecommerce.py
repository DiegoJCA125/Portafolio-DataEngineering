# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import sqlite3
import os
print("=" * 50)
print("ETL - ANALISIS DE VENTAS E-COMMERCE")
print("=" * 50)

#--------------- EXTRACCION ----------------
ruta_base = os.path.dirname(__file__)
ruta_csv = os.path.join(ruta_base, "../data/data.csv")

df_raw = pd.read_csv(ruta_csv, encoding="latin1")
print(f"--> Datos extraidos: {df_raw.shape[0]} filas.")

#------------- TRANSFORMACION -------------
print("\nIniciando la Transformacion...")
columnas_espanol = {
    'InvoiceNo': 'id_factura',
    'StockCode': 'id_producto',
    'Description': 'descripcion',
    'Quantity': 'cantidad',
    'InvoiceDate': 'fecha_factura',
    'UnitPrice': 'precio_unitario',
    'CustomerID': 'id_cliente',
    'Country': 'pais'
}
# APLICAMOS EL RENOMBRADO
df = df_raw.rename(columns = columnas_espanol)

# LIMPIAMOS LOS DATOS
# SE ELIMINAN FILAS DONDE EL ID DEL CLIENTE SEA NULO 
df = df.dropna(subset = ['id_cliente'])

# SE FILTRAN LOS VALORES POSITIVOS (REGLA DE NEGOCIO: NO SE QUIERE DEVOLUCIONES NI ERRORES)
df = df[(df['cantidad'] > 0) & (df['precio_unitario'] > 0)]

# CONVERSION DE TIPOS D DATOS
# SE CONVIERTE LA COLUMA DE FECHA DE TREXTO A OBJETO DINAMICOS
df['df_factura'] = pd.to_datetime(df['fecha_factura'])

# CREACIPON DE NUEVA METRICAS
df['ingreso_total'] = df['cantidad'] * df['precio_unitario']

print(f" -> Datos transformados. Filas Utiles: {df.shape[0]}")

# ------------------------ CARGA -------------------------------------
# SE DEFINE LA RUTA DE LA BD SQLite
ruta_db = os.path.join(ruta_base, "../database/ecommerce_sales.db")

# CREAMOS LA CAPERTA 'DATABASE' SI NO EXISTE
os.makedirs(os.path.dirname(ruta_db), exist_ok = True)

try:
    # CREAMOS LA CONEXION (SI NO EXISTE EL ARCHIVO .db, SQLite LO CREA SOLO)
    conn = sqlite3.connect(ruta_db)

    # CARGAMOS EL DATAFRAME NE UNA TABLA SQL
    # if_exists ='replace' SOBREESCRIBE LA TABLA SI YA EXISTE
    df.to_sql('ventas_procesadas', conn, if_exists = 'replace', index = False)

    print(f"\n EXITO!!! Base de Datos generada en: {ruta_db}")

except Exception as e:
    print(f"Ocurrio un error en la carga: {e}")

finally:
    #SIEMPRE CERRAR LA CONEXION PARA LIBERAR MEMORIA
    conn.close()
    print("Conexion a la base de datos cerrada-")

# Dentro de etl_ecommerce.py
ruta_script = os.path.dirname(__file__)
# Esto sube un nivel desde 'etl' y entra a 'database'
ruta_db = os.path.join(ruta_script, "..", "database", "ecommerce_sales.db")

os.makedirs(os.path.dirname(ruta_db), exist_ok=True)
conn = sqlite3.connect(ruta_db)
df.to_sql('ventas_procesadas', conn, if_exists='replace', index=False)
conn.close()
print(f"Base de datos guardada en: {os.path.abspath(ruta_db)}")