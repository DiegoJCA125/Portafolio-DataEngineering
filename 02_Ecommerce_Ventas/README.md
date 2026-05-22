#  End-to-End E-Commerce Data Engineering Pipeline

Este proyecto implementa un pipeline de datos completo (ETL), desde la ingesta de datos en crudo (Data Ingestion) hasta su almacenamiento en una base de datos relacional y su posterior visualizaci髇 en un dashboard interactivo de negocio.

El objetivo principal es demostrar habilidades s髄idas en arquitectura de datos limpia, manipulaci髇 de grandes vol鷐enes de informaci髇 con Python, optimizaci髇 de consultas SQL y entrega de valor al negocio.

---

##  Arquitectura del Proyecto

El flujo de los datos sigue la siguiente estructura secuencial:
1. **Origen:** Extracci髇 de datos de ventas en formato CSV (Dataset de e-commerce con +500,000 registros).
2. **Transformaci髇 (Python & Pandas):** Limpieza de nulos, formateo de tipos (fechas, IDs), eliminaci髇 de duplicados y c醠culo de la m閠rica de negocio 'ingreso_total'.
3. **Almacenamiento (SQL):** Carga optimizada en una base de datos relacional SQLite ('ecommerce_sales.db').
4. **Consumo (Streamlit & Plotly):** Creaci髇 de un Dashboard interactivo con filtros din醡icos por pa韘 y KPIs en tiempo real.

----

## ?? Estructura del Repositorio

"""text
02_Ecommerce_Ventas/
-- database/
|   --- ecommerce_sales.db       # Base de datos relacional generada
--- etl/
|   --- etl_ecommerce.py         # Script principal del proceso ETL
|   --- consultas_analiticas.py  # Reportes analiticos en SQL puro
|   --- dashboard.py             # Aplicacio interactiva de Streamlit
-- data/
|   --- data_origen.csv          # Datos crudo (ignorado en git si es muy pesado)
--- README.md                    # Documentaci髇on del proyecto