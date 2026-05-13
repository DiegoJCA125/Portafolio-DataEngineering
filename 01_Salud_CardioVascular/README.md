# Portafolio-DataEngineering
Portafolio

# ANALISIS DE RIEGOS CARDIOVASCULAR
## DESCRIPCION
Proyecto de Data Engineering que analiza factores d riesgo en enfermedades cardiaca usando datos reales de +1.000 paciente

## TECNOLOGIAS
- Python : Lengahje principal
- Pandas: Limpieza y transformacion de datos
- SQLite: Almacenamiento de datos
- Streamlit: Dashboard interactivo
- Matplotlib: Visualizaciones
- Power BI: Reportes empresariales

# Pipeline ETL
--------------------------------------------------------
## INSIGHTS ENCONTRADOS
- 51.3% de los pacientes tienen enfermedad cardiaca
- El grupo de edad 50-60 es el mas afectado (438 pacientes)
- Los numeros de 40 tienen la mayor tasa de riesgo (66%)
- Colesterol promedio: 246 mg/dl (Nivel limite)

## COMO EJECUTAR EL PROYECTO
1. Instalar dependencias:
'''bas
pip install pandas streamlit matplotlib sqlite3
'''

2. Ejecutal ETL:
''' bash 
python etl/etl_salud.py
'''

3. Ejecutar Dashboard:
'''bash
streamlit run dashboard/dashboard.py
'''
## ESTRUCTURA DEL PROYECTO
-------------------------------------------------------
##  Dataset
- Fuente: Kaggle - Heart Disease Dataset
- Registros: 1,025 pacientes
- Variables: 14 columnas clínicas