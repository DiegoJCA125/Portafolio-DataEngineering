# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os

#----------- CONFIGURACION DE PAGINA
st.set_page_config(
    page_title="Dashboard Salud Cardiovascular",
    page_icon="??",
    layout="wide"
)

# ------------- CARGAR DATOS DESDE SQL ---------------
# CONECTAMOS DIRECTAMENTE A LA BASE DE DATOS QUE GENERO EL ETL
ruta_db = os.path.join(os.path.dirname(__file__), "../data/salud.db")
conexion = sqlite3.connect(ruta_db)

# read_sql() - LEE TODA LA TABLA PACIENTES EN U NDATAFRAME
df = pd.read_sql("SELECT * FROM pacientes", conexion)
conexion.close()

print(f"Datos cargados: {df.shape}")

# --------- TITULO ----------------
st.title("?? Dashboard - Salud Cardiovascular")
st.markdown("Analisis de factores de riesgo en enfermedades cardiacas")
st.markdown("-------")