#  Proyecto 03: Real-Time Weather Monitoring Pipeline & Dashboard

Este proyecto implementa un flujo de ingenieria de datos de extremo a extremo para la captura, procesamiento y visualizacion de datos meteorologicos en tiempo real de las principales ciudades de Colombia: Bogota, Medellin, Cali, Barranquilla y Armenia.

---

##  Arquitectura del Sistema


1. **Origen de Datos:** API publica de OpenWeatherMap (Current Weather Data).
2. **Ingestion y ETL (Python):** Un script que consume la API, limpia las respuestas JSON, extrae las variables principales (temperatura, humedad, presion, velocidad del viento, condicion climatica) y calcula conversiones de unidades.
3. **Almacenamiento (Data Lakehouse / Relacional):** Inyeccion automatizada en una base de datos PostgreSQL alojada en Supabase Cloud.
4. **Orquestacion (CI/CD):** Un flujo de trabajo en GitHub Actions (`clima_cron.yml`) programado para ejecutarse automaticamente mediante un Cron Job cada 6 horas, ademas de permitir la activacion manual (`workflow_dispatch`).
5. **Consumo / Analytics:** Un tablero analitico interactivo construido en Streamlit que consume los datos de Supabase y permite filtrar el comportamiento climatico por ciudad.

---

##  Variables Monitoreadas

El pipeline procesa y almacena las siguientes metricas clave por cada ciudad:
* **Temperatura Actual (°C)**
* **Sensacion Termica (°C)**
* **Humedad Relativa (%)**
* **Presion Atmosferica (hPa)**
* **Velocidad del Viento (m/s)**
* **Fecha y Hora de Captura (Timestamp con Zona Horaria)**

---

