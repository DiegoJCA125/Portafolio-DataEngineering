# -*- coding: utf-8 -*-
import os
import streamlit as pd_stream
import pandas as pd
import plotly.express as px

pd_stream.set_page_config(
    page_title = "Big Data Dashboard - PySpark Medallion",
    page_icon = "📊",
    layout = "wide"
)

carpeta_base = os.path.dirname(os.path.abspath(__file__))
ruta_gold = os.path.join(carpeta_base, "data_gold", "reporte_kpis.csv")

# CARGUE DE DATOS
@pd_stream.cache_data
def cargar_datos(ruta):
    if os.path.exists(ruta):
        return pd.read_csv(ruta)
    return None

df_gold = cargar_datos(ruta_gold)

# INTERFAZ GRAFICA
pd_stream.title("Pipeline Arquitectura Medallón - 1M de Registros")
pd_stream.markdown("""
Esta aplicación visualiza las métricas consolidadas en la **Capa Gold** del pipeline de Big Data, 
luego de procesar, limpiar y agregar más de **1,000,000 de transacciones** distribuidas usando **PySpark**.
""")

if df_gold is None:
    pd_stream.error(f"No se encontró el archivo de la capa Gold en: {ruta_gold}")
    pd_stream.info("Por favor, ejecuta primero tu script `pipeline_medallion.py` para generar los datos.")
else:
    # BARRA LATERAL
    pd_stream.sidebar.header(" Filtros del Negocio")
    paises_disponibles = sorted(df_gold["pais"].unique())
    paises_seleccionados = pd_stream.sidebar.multiselect(
        "Selecciona los Paises:",
        options= paises_disponibles,
        default= paises_disponibles
    )

    # FILTRAR EL DATAFRAME SEGUN LA SELECCION
    df_filtrado = df_gold[df_gold["pais"].isin(paises_seleccionados)]

    # --------  SECCION 1: KPIS GLOBALES ----------------------
    pd_stream.subheader(" Indicadores Clave de Rendimiento (KPIs)")

    col1, col2, col3 = pd_stream.columns(3)

    total_ingresos = df_filtrado["ingresos_totales"].sum()
    total_ordenes = df_filtrado["total_ordenes"].sum()
    total_unidades = df_filtrado["unidades_vendidas"].sum()

    with col1:
        pd_stream.metric(label = "Ingresos Totales (USD)", value = f"${total_ingresos:,.2f}")
    with col2:
        pd_stream.metric(label = "Ordenes Procesadas", value = f"{total_ordenes:,}")
    with col3:
        pd_stream.metric(label = "Unidades Vendidas", value= f"{total_unidades:,}")

    pd_stream.markdown("--------------")

    # ---------- SECCION 2: GRAFICOS INTERACTIVOS --------------
    col_graf1, col_graf2 = pd_stream.columns(2)

    with col_graf1:
        pd_stream.subheader("Ingresos Totales por Pais")
        fig_pais = px.bar(
            df_filtrado.groupby("pais")["ingresos_totales"].sum().reset_index(),
            x="pais",
            y="ingresos_totales",
            color="pais",
            text_auto=".2s",
            labels={"ingresos_totales": "Ingresos (USD)", "pais": "Pais"},
            template="plotly_dark"
        )
        pd_stream.plotly_chart(fig_pais, use_container_width=True)

    with col_graf2:
        pd_stream.subheader("Participacion de Ventas por Categoria")
        fig_cat = px.pie(
            df_filtrado.groupby("categoria")["ingresos_totales"].sum().reset_index(),
            values="ingresos_totales",
            names="categoria",
            hole=0.4,
            template="plotly_dark"              
        )
        pd_stream.plotly_chart(fig_cat, use_container_width=True)

    # ------------- SECCION 3: TABLA DE DATOS GOLD ---------------------
    pd_stream.subheader("Detalle de la Capa Gold (Datos Agregados)")
    pd_stream.dataframe(df_filtrado, use_container_width=True)

pd_stream.caption("Desarrollado en Armenia, Quindío - Portafolio de Ingeniería de Datos.")