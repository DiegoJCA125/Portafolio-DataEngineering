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
"""
age ? edad del paciente
sex ? sexo (1=hombre, 0=mujer)
cp ? tipo de dolor en el pecho (0-3)
trestbps ? presion arterial en reposo
chol ? colesterol en sangre
fbs ? azucar en sangre en ayunas (1=alto, 0=normal)
restecg ? resultado electrocardiograma en reposo
thalach ? frecuencia cardiaca maxima
exang ? angina inducida por ejercicio (1=si, 0=no)
oldpeak ? depresion del segmento ST
slope ? pendiente del segmento ST
ca ? numero de vasos principales coloreados
thal ? tipo de talasemia
target ? tiene enfermedad cardiaca? (1=si, 0=no) ? columna objetivo
"""

# ---- TRANSFORMACION ----------
print("\n" + "=" * 50)
print("TRANSFORMACION DE DATOS")
print("=" * 50)