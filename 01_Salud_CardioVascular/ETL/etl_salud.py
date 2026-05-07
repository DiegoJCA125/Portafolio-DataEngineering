# -*- condig: utf-8 -*-
import pandas as pd
import numpy as np
import os

# ---- EXTRACION----------
# os.path.dirname(__file__) - carpeta donde esta el script
# os.path.join - une rutas de carpetas correctamente
ruta_csv = os.path.join(os.path.dirname(__file__), "../data/heart.csv")

df = pd.read_csv(ruta_csv)

print("=" * 50)
print("EXPLORACION INICIAL DEL DATASET")
print("=" * 50)

#CUANTOS PACIENTES Y COLUMNAS TIENE EL DATASET
print(f"\nFilas y Columnas: {df.shape}")
print(list(df.columns))

# VER LOS PRIMEROS REGISTROS
print(f"\nPrimeros 5 registros:")
print(df.head())

#TIPOS DE DATOS DE CADA COLUMNA
print(f"\nTipos de datos:")
print(df.dtypes)

#VALORES VACIOS POR COLUMNA
print(f"\nValores vacios:")
print(df.isnull().sum())

#ESTADISTICAS BASICAS
print(f"\n Estadisticas Basicas:")
print(df.describe())

# ---- TRANSFORMACION ----------
print("\n" + "=" * 50)
print("TRANSFORMACION DE DATOS")
print("=" * 50)

#----- PASO 1 ----- RENOMBRAR COLUMNAS 
# CAMBIAMOS LOS NOMBRES TECNICOS POR NOMBRES  ENTENDIBLES
df = df.rename(columns={
    "age": "edad",
    "sex": "sexo",
    "cp": "tipo_dolor_pecho",
    "trestbps": "presion_arterial",
    "chol": "colesterol",
    "fbs": "azucar_ayunas",
    "restecg": "electrocardiograma",
    "thalach": "frec_cardiaca_max",
    "exang": "angina_ejercicio",
    "oldpeak": "depresion_st",
    "slope": "pendiente_st",
    "ca": "vasos_principales",
    "thal": "talasemia",
    "target": "enfermedad_cardiaca"
})
print("Columnas renombradas correctamente!")

# ---- PASO 2 TRADUCIR VALORES NUMERICOS ----
# LOS VALORES 0 Y 1 NO SON ENTENDIBLES, LOS CONVERTIMOS A TEXTO
# map() - MAPEA VALORES DE UN DICCIONARIO A UNA COLUMNA
df["sexo"] = df["sexo"].map({1: "Hombres", 0: "Mujer"})
df["enfermedad_cardiaca"] = df["enfermedad_cardiaca"].map({1: "Si", 0: "No"})
df["angina_ejercicio"] = df["angina_ejercicio"].map({1: "Si", 0: "No"})
df["azucar_ayunas"] = df["azucar_ayunas"].map({1: "Alto", 0: "No"})
print("Valores traducidos correctamente")

# ----- PASO 3 CREAR COLUMNAS NUEVAS
# CREAR GRUPOS DE EDAD PARA ANALISIS
#pd.cut() - divide una columna numerica en rangos
df["grupo_edad"] = pd.cut(
    df["edad"],
    bins=[0, 40, 50, 60, 100],
    #bins los randos de edad
    labels = ["Menor 40", "40-50", "50-60", "Mayor 60"]
    # labels - nombre de cada rango
)
print("Grupos de edad creados!")

# CLASIFICAR COLESTEROL
df["nivel_colesterol"] = pd.cut(
    df["colesterol"],
    bins=[0, 200, 240, 999],
    labels = ["Normal", "Limite", "Alto"]
)
print("Niveles de colesterol clasificados!")

# ----------- PASO 4 VERIFICAR DATOS LIMPIOS -----------
print(f"\nDataset transformado:")
print(df[["edad", "sexo", "grupo_edad", "colesterol", "nivel_colesterol", "enfermedad_cardiaca"]].head(10))
print(f"\nTotal pacientes: {len(df)}")
print(f"Con enfermedad cardiaca: {df['enfermedad_cardiaca'].value_counts()['Si']}")
print(f"Sin enfermedad cardiaca: {df['enfermedad_cardiaca'].value_counts()['No']}")

import sqlite3

print("\n" + "=" * 50)
print("CARGA DE DATOS - L DE ETL")
print("=" * 50)

# CREA LA BASE DE DATOS EN A CARPETA DATA/
ruta_db = os.path.join(os.path.dirname(__file__), "../data/salud.db")
conexion = sqlite3.connect(ruta_db)
#connect()  CREA O ABRE LA BASE DATOS

#to_sql() - EXPORTA EL DATAFRAME A UNA TABLA SQL
# if_exists="replace" - SI LA TABLA EXISTE LA REEMPLAZA
#index = False  -NO GUARDA EL INDICE DE PANDAS
df.to_sql("pacientes", conexion, if_exists="replace", index=False)
print("Datos cargados en base de datos correctamente")

#VERIFICAR QUE SE CARGARON BIEN
query = "SELECT COUNT(*) as total FROM pacientes"
resultado = pd.read_sql(query, conexion)
#read_sql() - EJECUTA UNA CONSULTA SQL Y DEVUELVE UN DATAFRAME
print(f"Total registros en BD: {resultado['total'][0]}")

#CONSULTAS DE VERIFICACION
print("\nDistribucion por sexo:")
query_sexo = """
    SELECT sexo, 
           COUNT(*) as total,
           SUM(CASE WHEN enfermedad_cardiaca = 'Si' 
               THEN 1 ELSE 0 END) as con_enfermedad
    FROM pacientes
    GROUP BY sexo
"""
# CASE WHEN - ES UN IF/ELSE EN SQL
# SUM(CASE WHEN....) CUENTA LOS QUE CUMPLAS LA CONDICION
print(pd.read_sql(query_sexo, conexion))

print("\nDistribucion por grupo de edad:")
query_edad = """
    SELECT grupo_edad,
           COUNT(*) as total,
           SUM(CASE WHEN enfermedad_cardiaca = 'Si' 
               THEN 1 ELSE 0 END) as con_enfermedad
    FROM pacientes
    GROUP BY grupo_edad
    ORDER BY grupo_edad
"""
print(pd.read_sql(query_edad, conexion))

# GUARDAR EL DATAFRAME LIMPIO COMO CSV
ruta_clean = os.path.join(os.path.dirname(__file__), "../data/heart_clean.csv")
df.to_csv(ruta_clean, index=False)
#ESTE CSV LIMPIO LO USAREMOS PARA POWER BI
print("\nCSV limpio guardado para Power BI!")

conexion.close()
print("\nETL completado existosamente")