# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import sqlite3
import os
print("=" * 50)
print("ETL - ANALISIS DE VENTAS E-COMMERCE")
print("=" * 50)

#--------------- EXTRACCION ----------------
ruta_csv = os.path.join(os.path.dirname(__file__), "../data/data.csv")

df = pd.read_csv(ruta_csv, encoding="latin1")

print(f"\nFilas y Columnas: {df.shape}")
print(f"\nColumnas disponibles:")
print(list(df.columns))
print(f"\nPrimeros 5 registros:")
print(df.head())
print(f"\nTipos de datos:")
print(df.dtypes)
print(f"\nValores vacios:")
print(df.isnull().sum())

