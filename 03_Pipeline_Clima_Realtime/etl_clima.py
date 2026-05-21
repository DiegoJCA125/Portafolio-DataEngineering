# -*- coding: utf-8 -*-
import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine

# 1. Cargar el archivo .env
load_dotenv()
#  Leer la llave del archivo .env
LLAVE_SECRETA = os.getenv("OPENWEATHER_API_KEY")

USUARIO = os.getenv("DB_USER")
CLAVE = os.getenv("DB_PASSWORD")
SERVIDOR = os.getenv("DB_HOST")
PUERTO = os.getenv("DB_PORT")
BASE_DATOS = os.getenv("DB_NAME")

# CREACION DE URL DE CONEXION A SUPABASE
DATABASE_URL = f"postgresql://{USUARIO}:{CLAVE}@{SERVIDOR}:{PUERTO}/{BASE_DATOS}"

# Ciudades de Colombia que vamos a monitorear
CIUDADES = ["Bogota", "Medellin", "Cali", "Barranquilla", "Armenia"]

print("==================================================")
print("     ETL EN TIEMPO REAL: CLIMA --> SUPABASE       ")
print("==================================================")

def extraer_clima(ciudad, token_api):
    """Funcion para conectarse a OpenWeather y traer los datos en vivo"""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad},CO&appid={token_api}&units=metric&lang=es"
    try:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            return respuesta.json()
        else:
            print(f"? Error con {ciudad}: Codigo {respuesta.status_code}")
            return None
    except Exception as e:
        print(f"? Error de conexion en {ciudad}: {e}")
        return None

# Verificacion rapida por si acaso el .env no leyo nada
if not LLAVE_SECRETA or not SERVIDOR:
    print("? ERROR: Faltan variables de entorno en tu archivo .env")
else:
    # LISTA VACIA PARA ACUMULARR LOS DATOS TRANSFORMADOS DE CADA CIUDAD
    datos_transformados = []

    # 2 CICLO PRINCIPAL DE EXTRACCION Y TRANSFORMACION
    for cd in CIUDADES:
        print(f" ---> Procesando datos para {cd}...")
        data_clima = extraer_clima(cd, LLAVE_SECRETA)

        if data_clima:
            try:
                # EXTRUCTURACION Y LIMPIEZA DE DATOS (DATA TRANSFORMACION)
                registro = {
                    "ciudad": data_clima["name"],
                    "pais": data_clima["sys"]["country"],
                    "temperatura_c": data_clima["main"]["temp"],
                    "sensacion_termica_c": data_clima["main"]["feels_like"],
                    "humedad_porcentaje": data_clima["main"]["humidity"],
                    "presion_hpa": data_clima["main"]["pressure"],
                    "velocidad_viento_m_s": data_clima["wind"]["speed"],
                    "estado_clima": data_clima["weather"][0]["description"],
                    "fecha_extraccion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                datos_transformados.append(registro)
            except KeyError as e:
                print(f"   ?? Error en la estructura en {cd}: {e}")
    # 3 CARGAR A LA NUBE
    if datos_transformados:
        df_clima = pd.DataFrame(datos_transformados)

        # GUARDA EL RESPALDO LOCAL EN CSV POR SEGURIDAD
        carpeta_actual = os.path.dirname(__file__)
        ruta_csv = os.path.join(carpeta_actual, "data", "clima_colombia.csv")
        os.makedirs(os.path.dirname(ruta_csv), exist_ok=True)
        df_clima.to_csv(ruta_csv, index=False, encoding="utf-8")

        try:
            print("\n --> Conectando a AWS/Supabase para cargar los datos...")
            engine = create_engine(DATABASE_URL)

            # SE CARGA A LA TABLA 'CLIMA_HISTORICO'
            # if_exists='append' ES EL SECRETO PARA ACUMULAR EL HISTORIAL
            df_clima.to_sql("clima_historico", con=engine, if_exists="append", index=False)

            print(" Pipeline completado con exito!! Datos guardados en la nube")

        except Exception as e:
            print(f" Error al cargar los datos en al nube: {e}")

print("\n==================================================")