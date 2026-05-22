# -*- conding: utf-8 -*-
import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine

print("==================================================")
print("     ETL FINANCIAL: CRYPTO -> AWS/SUPABASE        ")
print("==================================================")

# CARGAR LAS CREDENCIALES (.env)
carpeta_actual = os.path.dirname(__file__)
ruta_env = os.path.join(carpeta_actual, "..", ".env")
load_dotenv(dotenv_path=ruta_env)

USUARIO = os.getenv("DB_USER")
CLAVE = os.getenv("DB_PASSWORD")
SERVIDOR = os.getenv("DB_HOST")
PUERTO = os.getenv("DB_PORT")
BASE_DATOS = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{USUARIO}:{CLAVE}@{SERVIDOR}:{PUERTO}/{BASE_DATOS}"

# DEFINIMOS LAS CRIPTOS OBJETIVO Y LAS MONEDAS DE CAMBIO (USD Y COP)
CRIPTOS = "bitcoin,ethereum,solana"
MONEDAS_CAMBIO = "usd,cop"

def extraer_precios_crypto():
    """Consulta la API publica de CoinGecko para traer precios en vivo"""
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={CRIPTOS}&vs_currencies={MONEDAS_CAMBIO}"
    try:
        # A?ADIMOS UN USER-AGENT GENERICO PARA EVITAR QUE LA API NOS BLOQUEE POR SEGURIDAD
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        respuesta = requests.get(url, headers=headers)
        if respuesta.status_code == 200:
            return respuesta.json()
        else:
            print(f" Error al consultar CoinGecko: Codigo {respuesta.status_code}")
            return None
    except Exception as e:
        print(f" Error de conexion con la API financiera: {e}")
        return None
    
if not  SERVIDOR:
    print("ERROR: No se pudieron cargar las credenciales del archivo .env")
else:
    # 2 EXTRACCION Y TRANSFORMACION
    datos_crudos = extraer_precios_crypto()

    if datos_crudos:
        registros_procesados = []
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # SE TRANSFORMA LA ESTRUCTURA ANIDADES DEL JSON DE COINGECKO A FILAS PLANAS
        for crypto_id in ["bitcoin", "ethereum", "solana"]:
            if crypto_id in datos_crudos:
                detalles = datos_crudos[crypto_id]
                registro = {
                    "activo_id": crypto_id.upper(),
                    "precio_usd": detalles.get("usd", 0.0),
                    "precio_cop": detalles.get("cop", 0.0),
                    "ultima_actualizacion": fecha_actual
                }
                registros_procesados.append(registro)
        # 3 CARGA O LOAD A LA NUBE
        if registros_processed:= registros_procesados:
            df_crypto = pd.DataFrame(registros_procesados)

            try:
                print(" --> Conectando a Supabase para inyectar precios...")
                engine = create_engine(DATABASE_URL)

                # INSERTAMOS LOS DATOS ACUMULANDOLOS EN LA TABLA 'cripto_historico' EN SUPABASE
                df_crypto.to_sql("crypto_historico", con=engine, if_exists="append", index=False)

                print("Pipeline Crypto completado! Datos resguardados en la nube.")
                print(df_crypto.to_string(index=False))

            except Exception as e:
                print("Error al cargar los datos financieros: {e}")
    else:
        print("Proceso interrumpido por fallo en la API.")

print("=======================================================================")
