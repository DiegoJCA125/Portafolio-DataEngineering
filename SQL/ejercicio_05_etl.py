import pandas as pd
import sqlite3

# EXTRACT: LEE LOS DATOS CRUDOS
def extract(ruta_csv: str) -> pd.DataFrame:
    """"LEE EL CSV CRUDO Y LO DEVUELVE COMO UN DATAFRAME SIN MODIFICAR NADA"""
    df = pd.read_csv(ruta_csv)
    print(f"[EXTRACT] {len(df)} filas leídas desde {ruta_csv}")
    return df

# TRANSFORM: LIMPIA Y TRANSFORMA LOS DATOS
def transform(df: pd.DataFrame) -> pd.DataFrame:
    """"LIMPIA Y TRANSFORMA EL DATAFRAME"""
    # Eliminar filas con valores nulos
    df = df.copy() # Copy() evita modificar el dataframe original
    columnas_texto = ["cliente", "ciudad", "producto"]
    for col in columnas_texto:
        df[col] = df[col].str.strip()

    ## ELIMINA FILAS SIN CLIENTE (SIN EL CLIENTE EL PEDIDO NO SIRVE)
    filas_antes = len(df)
    df = df.dropna(subset=["cliente"])
    print(f"[TRANSFORM] {filas_antes - len(df)} filas sin cliente eliminadas")

    ### ENTANDARIZAR MAYUSCULAS Y MINUSCULAS
    df["ciudad"] = df["ciudad"].str.title()
    df["cliente"] = df["cliente"].str.title()

    # ESTANDARIZAR FECHAS: CONVERTIR A FORMATO YYYY-MM-DD
    fecha_iso = pd.to_datetime(df["fecha"], format="%Y-%m-%d", errors="coerce")
    fecha_dmy = pd.to_datetime(df["fecha"], format="%d/%m/%Y", errors="coerce")
    df["fecha"] = fecha_iso.fillna(fecha_dmy)

    ### RELLENAR PRECIOS FALTANTES CON EL PROMEDIO DEL MISMO PRODUCTO
    df["precio"] = df["precio"].fillna(df.groupby("producto")["precio"].transform("mean"))

    df["cantidad"] = df["cantidad"].fillna(1).astype(int)

    ## ELIMINAR FILAS DUPLICADAS EXACTAS (MISMO CLIENTE, PRODUCTO, FECHA)
    filas_antes = len(df)
    df = df.drop_duplicates(subset=["cliente", "producto", "fecha"])
    print(f"[TRANSFORM] {filas_antes - len(df)} filas duplicadas eliminadas")

    ## recalcular pedido_idpara que quyede de consecutivo
    df = df.reset_index(drop=True)
    df["pedido_id"] = df.index + 1

    print(f"[TRANSFORM] {len(df)} filas limpias para cargar")
    return df

## GUARDAR EN LA BD
def load(df:pd.DataFrame, ruta_db: str, tabla: str) -> None:
    """CARGAR EL DATAFRAME LIMPIO A UNA TABLA SQLITE"""
    conexion = sqlite3.connect(ruta_db)
    df.to_sql(tabla, conexion, if_exists="replace", index=False)
    conexion.close()
    print(f"[LOAD] {len(df)} filas cargadas en la tabla '{tabla}' de {ruta_db}")

#### PIPELINE
def main():
    RUTA_CSV = "ventas_raw.csv"
    RUTA_DB = "pipeline.db"
    TABLA = "ventas_limpias"

    print("------INICIANDO PIPELINE ETL ------ \n")
    df_crudo = extract(RUTA_CSV)
    df_limpio = transform(df_crudo)
    load(df_limpio, RUTA_DB, TABLA)
    print("\n------ PIPELINE ETL FINALIZADO ------")

    conexion = sqlite3.connect(RUTA_DB)
    print("----- VERIFICACION: datos ya limpios en SQL ----")
    resultado = pd.read_sql(f"SELECT * FROM {TABLA} LIMIT 5", conexion)
    print(resultado, "\n")

    print("---- INGRESOS TOTALES POR PRODUCTO (DATOS LIMPIOS)----")
    ingresos = pd.read_sql(f"""
        SELECT producto, ROUND(SUM(precio * cantidad), 0) AS ingresos
        FROM {TABLA}
        GROUP BY producto
        ORDER BY ingresos DESC
        """, conexion)
    print(ingresos)

    if __name__ == "__main__":
        main()