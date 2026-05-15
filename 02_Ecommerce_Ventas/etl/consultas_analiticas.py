import sqlite3
import pandas as pd
import os

# 1. Definir la ruta exacta (igual que en el ETL)
ruta_script = os.path.dirname(__file__)
ruta_db = os.path.join(ruta_script, "..", "database", "ecommerce_sales.db")

print(f"Buscando en: {os.path.abspath(ruta_db)}")

# 2. Solo intentar la consulta si el archivo existe
if os.path.exists(ruta_db):
    conn = sqlite3.connect(ruta_db)
    print("? Conexion establecida.\n")

    print("=" * 50)
    print("REPORTES ANALISTICOS - SQL")
    print("=" * 50)

# ------- CONSULTA 1:  TOP 5 PRODUCTOS CON MAS INGRESOS -------
# TERMINO CLAVE SUM(SUMA) Y GROUP BY (AGRUPAR POR)
    query_productos = """
    SELECT
        descripcion,
        SUM(cantidad) as total_unidades,
        SUM(ingreso_total) as ingresos_generados
    FROM ventas_procesadas
    GROUP BY descripcion
    ORDER BY ingresos_generados DESC
    LIMIT 5;
    """
    top_productos = pd.read_sql(query_productos, conn)
    print("\n?? TOP 5 PRODUCTOS MAS RENTABLES:")
    print(top_productos)

# ----- CONSULTA 2: VENTAS POR PAIS -----------
    query_paises = """
    SELECT 
        pais,
        COUNT(DISTINCT id_factura) as numero_pedidos,
        SUM(ingreso_total) as ventas_totales
    FROM ventas_procesadas
    GROUP BY pais
    ORDER BY ventas_totales DESC
    LIMIT 5;
    """
    ventas_paises = pd.read_sql(query_paises, conn)
    print("\n ?? TOP PAISES CON MAS VENTAS:")
    print(ventas_paises)

# ------- CONSULTA 3: TICKET PROMEDIO POR CLIENTE
# TERMINO CLAVE= AVG (PROMEDIO / AVERAGE)
    query_ticket = """
    SELECT 
        AVG(ingreso_total) as ticket_promedio
    FROM ventas_procesadas;
    """
    ticket_medio = pd.read_sql(query_ticket, conn)
    print(f"\n ?? TICKET PROMEDIO DE VENTA: $ {ticket_medio.iloc[0,0]:.2f}")

# 3 CERRAMOS AL FINAL DE TODO
    conn.close()
    print("\n ? Proceso finalizado y base de datos cerrada")

else:
    print("? ERROR: El archivo no existe, Por favor, corre 'etl_ecommerce.py' primero")