#-*- coding: utf-8 -*-

import os
import streamlit as Streamlit
import pandas as pd
import plotly.express as px

# RUTA DE LA ARQUITECTURA
carpeta_base = os.path.dirname(os.path.abspath(__file__))
ruta_gold_data = os.path.join(carpeta_base, "data", "gold", "resumen_ventas.csv")

# CONFIGURACION DE LA PAGINA DE STREAMLIT
Streamlit.set_page_config(
    page_title="KPI dashboard - Ventas Masivas",
    page_icon="📊",
    layout="wide"
)

# CARGA DE LOS DATOS
@Streamlit.cache_data
def cargar_datos_gold():
    if os.path.exists(ruta_gold_data):
        return pd.read_csv(ruta_gold_data)
    else:
        Streamlit.error(f"No se encontro la data consolidad de la capa Gold en: {ruta_gold_data}")
        return None
    
df_gold = cargar_datos_gold()

# INTERFAZ GRAFICA 
Streamlit.title("Dashboard de Control Comercial")
Streamlit.markdown("Analitica de rendimiento optimizada bajo la Arquitectura Medallion **PySpark**")

if df_gold is not None:
    # 1 SECCION DE METRICAS (KPIS)
    ventas_totales = df_gold["Ventas_Totales"].sum() if "Ventas_Totales" in df_gold.columns else 0
    transacciones_totales = df_gold["Transacciones_Totales"].sum() if "Transacciones_Totales" in df_gold.columns else 0

    col1, col2, col3 = Streamlit.columns(3)
    with col1:
        Streamlit.metric(label="Ingresos Totales", value=f"$ {ventas_totales:,.2f}")
    with col2:
        Streamlit.metric(label="Volumen de Transacciones", value=f"{transacciones_totales}:,")
    with col3:
        Streamlit.metric(label="Infraestructura Backend", value="PySpark + Parquet")

    Streamlit.markdown("-----")

    # 2 SECCION DE GRAFICAS INTERACTIVAS
    col_izq, col_der = Streamlit.columns(2)

    with col_izq:
        Streamlit.subheader("Ventas Totales por Categoria")
        if "categoria" in df_gold.columns and "Ventas_Totales" in df_gold.columns:
            fig_bar = px.bar(
                df_gold, 
                x="categoria", 
                y="Ventas_Totales", 
                color="categoria",
                text_auto='.2s',
                title="Distribución Financiera del Millón de Filas",
                template="plotly_dark"
            )
            Streamlit.plotly_chart(fig_bar, use_container_width=True)
        else:
            Streamlit.warning("Revisa las columnas del archivo Gold. Deben coincidir con 'categoria' y 'Ventas_Totales'")

    with col_der:
        Streamlit.subheader("Vista Consolidada de Datos (Gold)")
        Streamlit.dataframe(df_gold, use_container_width=True)