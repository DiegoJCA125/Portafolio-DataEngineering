# -*- coding: utf-8 -*-
import os 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from dotenv import load_dotenv
import numpy as np

# 1 ------- CARGAMOS LA CONFIGURACION SEGURA (.env)
load_dotenv()

USUARIO = os.getenv("DB_USER")
CLAVE = os.getenv("DB_PASSWORD")
SERVIDOR = os.getenv("DB_HOST")
PUERTO = os.getenv("DB_PORT")
BASE_DATOS = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{USUARIO}:{CLAVE}@{SERVIDOR}:{PUERTO}/{BASE_DATOS}"

print("==================================================")
print("   ANALISIS GRAFICO DE VARIABLES PARA ML          ")
print("==================================================")

try:
    # 2 CONECTAR A AWS Y TRAER LOS DATOS
    print("-> Conectando a Supabase para descargar los datos...")
    engine = create_engine(DATABASE_URL)
    query = "SELECT * FROM ventas_procesadas"
    df = pd.read_sql(query, con=engine)
    print(f" --> Datos listos!! Descargadas {df.shape[0]} filas y {df.shape[1]} columnas \n")

    # CONFIGURACION ESTETIGAS DE LOS GRAFICOS
    sns.set_theme(style="whitegrid")

    # -----------------------------------------------------------------
    # AQUI EMPEZAMOS NUESTRO ANALISIS ESTADISTICO
    # -----------------------------------------------------------------

    # 3 CREACION DE UN BOXPLOT ( GRAFICOS D CAJAS )
    print("--> Generando Grafico de Cajas para detectar datos atipicos...")

    plt.figure(figsize = (10, 5))
    #CREAMOS EL GRAFICO DE CAJA HORIZONTAL
    sns.boxplot(x=df['ingreso_total'], color='skyblue')

    #TITULOS DEL GRAFICO
    plt.title('Distribucion de Ingresos Totales y Detencion de Outliers', fontsize=14)
    plt.xlabel('Monto de la Ventas ($)')

    # GUARDAMOS EL GRAFICO EN TU CARPETA PARA QUE LO PUEDAS VER
    # BUSCAMOS LA CARPERTA EXACTO DONDE ES ESTA CORRIENDO EL SCRIPT 
    carpeta_actual = os.path.dirname(__file__)

    ruta_boxplot = os.path.join(carpeta_actual, 'boxplot_ingresos.png')
    plt.savefig(ruta_boxplot, bbox_inches='tight')
    print("? Grafico guardado camo 'bloxplot_ingresos.png' en tu carpeta")
    plt.show()

    # 4 CREACION DE UN HISTOGRAMA CON CURVA DE DENSIDAD (KDE)
    print("--> Generando Histograma con curva de Densidad")
    plt.figure(figsize=(10, 5))

    # SE CREA EL HISTOGRAMA (bins = 50 ES EL NUMERO DE BARRAS)
    # SE LE SUMA LA CURVA DE DENSIDAD SUAVIZADA (kde=True)
    sns.histplot(df['ingreso_total'], bins=50, kde=True, color='purple', stat="density")

    # TITULOS DEL GRAFICO
    plt.title('Distribucion Detallada y Densida de Ingresos Totales', fontsize=14)
    plt.xlabel('Monto de la Venta ($)')
    plt.ylabel('Densidad de Registros')

    # GUARDAMOS EL SEGUNDO GRAFICO
    
    ruta_histograma = os.path.join(carpeta_actual, 'histograma_densidad_ingresos.png')
    plt.savefig(ruta_histograma, bbox_inches='tight')
    print("? Grafico guardado como 'histograma_densidad_ingresos.png' en tu carpeta")
    plt.show()

    # -----------------------------------------------------------------
    # 5. TRANSFORMACION MATEMATICA PARA MACHINE LEARNING
    # -----------------------------------------------------------------
    print("--> Aplicando transformacion logaritmica para corregir el sesgo...")

    #UTILIZAMOS log1p (logaritmo de x +1) PARA EVITAR ERRORES SI LELGA HABER ALGUN INGRESO DE 0
    df['ingreso_log'] = np.log1p(df['ingreso_total'])

    print("--> Generando Histograma de la variable transformada...")
    plt.figure(figsize=(10, 5))

    # SE GRAFICA LA NUEVA COLUMNA TRANSFORMADA
    sns.histplot(df['ingreso_log'], bins=30, kde=True, color='green', stat="density")
    plt.title('Distribucion Normalizada de Ingresos (Transformacion Logaritmica)', fontsize=14)
    plt.xlabel('logaritmo del Monto de Venta')
    plt.ylabel('Densidad')

    # GUARDAMOS EN LA CARPETA CORRECTA
    ruta_log = os.path.join(os.path.dirname(__file__), 'histograma_log_ingresos.png')
    plt.savefig(ruta_log, bbox_inches='tight')
    plt.close()
    print("? Grafico de transformacion guardado como 'histograma_log_ingresos.png'")

    # -----------------------------------------------------------------
    # 6. ANALISIS BIVARIADO: RELACION ENTRE CANTIDAD E INGRESO
    # -----------------------------------------------------------------
    print("-> Generando Grafco de Dispersion (Cantidad vs Ingreso)...")
    plt.figure(figsize = (10, 6))

    # SE CRUZA CANTIDAD DEL EJE X CON EL INGRESO ORIGINAL DEL EJE Y
    # SE USA alpha=0.5 PARA QUE LOS PUNTOS SEAN SEMITRANSPARENTES Y VER DONDE HAY MAS ACUMULACION
    sns.scatterplot(data=df, x='cantidad', y='ingreso_total', alpha=0.5, color='darkorange')

    plt.title('Relacion entre Cantidad de Productos e Ingreso Total por Venta', fontsize=14)
    plt.xlabel('Cantidad de Productos en la Factura')
    plt.ylabel('Monto Total de la Ve nta ($)')

    # GUARDAMOS EN AL CARPETA CORRESPONDIENTE
    ruta_scatter = os.path.join(carpeta_actual, 'scatter_cantidad_ingreso.png')
    plt.savefig(ruta_scatter, bbox_inches='tight')
    plt.close()
    print("? Grafico Bivariado guardado como 'scatter_cantidad_ingreso.png'")

    print("\n=================================================")
    print("Fase de Analisis Grafico Completada con Exito!!")
    print("\n=================================================")
    
except Exception as e:
    print(f"Error!! en el proceso: {e}")
