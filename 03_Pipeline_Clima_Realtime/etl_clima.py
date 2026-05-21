# -*- coding: utf-8 -*-
import os
import requests
from dotenv import load_dotenv

# 1. Cargar el archivo .env
load_dotenv()

# Ciudades de Colombia que vamos a monitorear
CIUDADES = ["Bogota", "Medellin", "Cali", "Barranquilla", "Armenia"]

print("==================================================")
print("   PIPELINE DE DATOS EN TIEMPO REAL: CLIMA       ")
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


# 2. Leer la llave del archivo .env justo aqui
LLAVE_SECRETA = os.getenv("OPENWEATHER_API_KEY")

# Verificacion rapida por si acaso el .env no leyo nada
if not LLAVE_SECRETA:
    print("? ERROR: No se encontro la variable 'OPENWEATHER_API_KEY' en tu archivo .env")
else:
    # 3. Ciclo principal para extraer los datos de cada ciudad
    for cd in CIUDADES:
        print(f"--> Extrayendo datos en vivo para {cd}...")
        
        # Le pasamos la ciudad y la llave que acabamos de leer
        data_clima = extraer_clima(cd, LLAVE_SECRETA)
        
        if data_clima:
            try:
                temperatura = data_clima['main']['temp']
                descripcion = data_clima['weather'][0]['description']
                print(f"   [OK] Temp: {temperatura} Grados Centigrados | Clima: {descripcion}")
            except KeyError:
                print("   ?? Los datos se recibieron pero la estructura JSON cambio.")

print("\n==================================================")