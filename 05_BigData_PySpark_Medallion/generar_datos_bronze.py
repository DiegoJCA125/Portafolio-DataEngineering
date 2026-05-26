# -*- condig: utf-8 -*-
import os
import random
import pandas as pd
from datetime import datetime, timedelta

print("Fabricando 1 millon de registros para la capa Bronze")

#   CONFIGURACION DE RUTAS
carpeta_actual = os.path.dirname(__file__)
ruta_bronze = os.path.join(carpeta_actual, "data_bronze", "transacciones_raw.csv")

#   PARAMETROS PARA AL SIMULACION
productos = ["Laptop Pro", "Teclado Mecanico", "Monitor 4K", "Raton Inalambrico", "Audifonos Gamer", "Hub USB-C"]
categorias = ["Computo", "Accesorios", "Video", "Accesorios", "Audio", "Conectividad"]
paises = ["Colombia", "Mexico", "Argentina", "Chile", "Peru"]

#   GENERACION MASIVA OPTIMIZADA CON LISTAS
fechas_base = datetime(2026, 1, 1)
data = []

for idx in range(1, 1000001):
    prod_idx = random.randint(0, len(productos) - 1)
    cantidad = random.randint(1, 5)
    precio_unitario = round(random.uniform(15.0, 1200.0), 2)

    #   METER RUIDO AGREGE: 1% DE DATOS DUPLICADOS O ID PARA LIMPIEZA POSTERIOR
    id_transaccion = f"TRX-{1000000 + idx}" if random.random() > 0.01 else f"TRX-{1000000 + idx - 1}"

    #   FECHAS DISTRIBUIDAD EN LOS PRIMEROS MESES DE 2026
    fecha_random = fechas_base + timedelta(seconds=random.randint(0, 12000000))

    data.append([
        id_transaccion,
        fecha_random.strftime("%Y-%m-%d %H:%M:%S"),
        random.choice(paises),
        productos[prod_idx],
        categorias[prod_idx],
        cantidad,
        precio_unitario if random.random() > 0.005 else None # 0.5% de valores nulos
    ])

#   CONVENTIR A DATAFRAME Y GUARDAR EN BRONZE
df_raw = pd.DataFrame(data, columns = ["id_transaccion", "fecha_compra", "pais", "producto", "categoria", "cantidad", "precio_unitario"])
df_raw.to_csv(ruta_bronze, index=False, encoding="utf-8")

print(f"¡Capa Bronze lista! Archivo guardado con exito en: {ruta_bronze}")