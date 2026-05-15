#  End-to-End E-Commerce Data Engineering Pipeline

Este proyecto implementa un pipeline de datos completo (ETL), desde la ingesta de datos en crudo (Data Ingestion) hasta su almacenamiento en una base de datos relacional y su posterior visualización en un dashboard interactivo de negocio.

El objetivo principal es demostrar habilidades sólidas en arquitectura de datos limpia, manipulación de grandes volúmenes de información con Python, optimización de consultas SQL y entrega de valor al negocio.

---

##  Arquitectura del Proyecto

El flujo de los datos sigue la siguiente estructura secuencial:
1. **Origen:** Extracción de datos de ventas en formato CSV (Dataset de e-commerce con +500,000 registros).
2. **Transformación (Python & Pandas):** Limpieza de nulos, formateo de tipos (fechas, IDs), eliminación de duplicados y cálculo de la métrica de negocio 'ingreso_total'.
3. **Almacenamiento (SQL):** Carga optimizada en una base de datos relacional SQLite ('ecommerce_sales.db').
4. **Consumo (Streamlit & Plotly):** Creación de un Dashboard interactivo con filtros dinámicos por país y KPIs en tiempo real.

---

## ?? Estructura del Repositorio

"""text
02_Ecommerce_Ventas/
??? database/
?   ??? ecommerce_sales.db       # Base de datos relacional generada
??? etl/
?   ??? etl_ecommerce.py         # Script principal del proceso ETL
?   ??? consultas_analiticas.py  # Reportes analíticos en SQL puro
?   ??? dashboard.py             # Aplicación interactiva de Streamlit
??? data/
?   ??? data_origen.csv          # Datos crudo (ignorado en git si es muy pesado)
??? README.md                    # Documentación del proyecto