import pandas as pd

#DEFINIMOS LA RUTA DEL ARCHIVO (Como esta en la misma carpeta, solo con el nombre tenemos)
FILE_NAME = 'product_sales.csv'
def diagnostico_datos():
    # 1 EXTRACCION
    try:
        #Se usara el utf-8 por el si el csv tiene caracteres especiales
        df = pd.read_csv(FILE_NAME, encoding='utf-8')
        print("? Dataset cargado con exito!\n")
    except Exception as e:
        print(f"? Error al cargar: {e}")
        return
    
    # 2 EXPLROACION TECNICA (AUDIT)
    print("---- Extructa del Dataset ----")
    print(df.info())

    print("\n --- Primeros Registros ----")
    print(df.head())

    print("\n --- Analisis de Calidad ---")
    nulos = df.isnull().sum()
    print("Valores Nulos por Columna:")
    print(nulos[nulos > 0] if nulos.sum() > 0 else "No hay valores nulos, limpieza inicial perfecta")

    # 3 ESTADISTICAS RAPIDAS
    print("\n ---- Resumen Estadistico ------")
    print(df.describe())

if __name__ == "__main__":
    diagnostico_datos()
