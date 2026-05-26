# PROYECTO 05: BIG DATA PIPELINE - ARQUITECTURA MEDALLON CON PYSPARK

##  DESCRIPCION DEL PROYECTO
Este proyecto demuestra la implementacion de una **Arquitectura Medallon (Lakehouse)** a gran escala utilizando **Apache Spark (PySpark)** para procesar, limpiar y consolidar de forma eficiente un dataset simulado de **1,000,000 de transacciones electronicas** de un e-commerce global. 

Ademas, incluye una capa de servicio analitico que consume los datos finales estructurados a traves de un dashboard interactivo moderno.

---

##  ARQUITECTURA DE DATOS (MEDALLON)

El pipeline procesa el flujo masivo dividiendolo en tres capas incrementales de calidad:

1. **Capa Bronze (Raw Data):** Ingesta del archivo masivo `transacciones_raw.csv` generado sinteticamente con mas de un millon de filas. Contiene datos crudos con ruido adrede: registros duplicados, valores nulos e inconsistencias de formato.
2. **Capa Silver (Enriched Data):** Motor de procesamiento en memoria con PySpark. Se aplican reglas de calidad de datos (Data Quality): eliminacion de duplicados por ID de transaccion, tipado de marcas de tiempo (`timestamps`), calculo analitico de ventas totales por item y limpieza de nulos estructurales.
3. **Capa Gold (Curated Data):** Agregacion analitica de negocio. Se agrupan los datos limpios por Pais y Categoria para computar KPIs criticos: Ingresos totales distribuidos, volumen de ordenes validas y unidades totales vendidas.

---

##  STACK TECNOLOGICO
- **Procesamiento Nucleo:** Apache Spark / PySpark
- **Manipulacion & Persistencia:** Python, Pandas
- **Visualizacion:** Streamlit, Plotly Express
- **Entorno de Desarrollo:** VS Code / Git

---

1. Clonar el repositorio e instalar dependencias
pip install pyspark streamlit plotly pandas

2. Generar el dataset masivo (Capa Bronze)
python 05_BigData_PySpark_Medallion/generar_datos_bronze.py

3. Correr el Pipeline de Big Data (PySpark)
python 05_BigData_PySpark_Medallion/pipeline_medallion.py

4. Lanzar el Dashboard Analitico
streamlit run 05_BigData_PySpark_Medallion/dashboard.py