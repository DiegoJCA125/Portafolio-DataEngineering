# -*- coding: utf-8 -*-
import os
import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine
from dotenv import load_dotenv

# 1 CONFIGURACION DE LA PAGINA DE STREAMLIT
st.set_page_config(page_title="Dashboard Clima Colombia", page_icon="???", layout="wide")

# 2 CARGAR CREDENCIALES SEGURAS
carpeta_actual = os.path.dirname(__file__)
ruta_env = os.path.join(carpeta_actual, "..", ".env")
load_dotenv()

#LEER LAS VARIABLES
USUARIO = os.getenv("DB_USER")
CLAVE = os.getenv("DB_PASSWORD")
SERVIDOR = os.getenv("DB_HOST")
PUERTO = os.getenv("DB_PORT")
BASE_DATOS = os.getenv("DB_NAME")

# VERIFICACION DE SEGURIDAD POR SI ACASO
if not PUERTO:
    st.error("? No se pudo leer las variables del archivo .env. Verifica la ruta.")

DATABASE_URL = f"postgresql://{USUARIO}:{CLAVE}@{SERVIDOR}:{PUERTO}/{BASE_DATOS}"

@st.cache_data(ttl=60) # CACHEAMOS LOS DATOS POR 1 MINUTOS PARA NO SATURAR SUPABASE
def cargar_datos():
    engine = create_engine(DATABASE_URL)
    query = "SELECT * FROM clima_historico ORDER BY fecha_extraccion DESC"
    df = pd.read_sql(query, con=engine)
    # SE CONVIERTE LA FECHA A FORMATO TIME DE PANDAS
    df["fecha_extraccion"] = pd.to_datetime(df["fecha_extraccion"])
    return df

try: 
    df = cargar_datos()
    #TITULO DESL DASHBOARD
    st.title("??? Monitoreo de Clima en Tiempo Real - Colombia")
    st.markdown("Este tablero analiza los datos metereologicos extraidos en vivo y almacenados en AWS/Supabase")
    st.write("---------")

    # 3 FILTRO DE CIUDAD (SIDEBAR)
    st.sidebar.header("Filtros del Proyecto")
    ciudades_disponibles = df["ciudad"].unique()
    ciudad_seleccionada = st.sidebar.selectbox("Selecciona una ciudad para ver su historial", ciudades_disponibles)

    #FILTRAR DATOS PARA AL CIUDAD SELECCIONADA
    df_ciudad = df[df["ciudad"] == ciudad_seleccionada].sort_values("fecha_extraccion")

    # 4 TARJETAS INFORMATICAS (METRICAS ACTUALES)
    # TOMAMOS EL REGISTRO MAS RECIENTE EN LA BASE DE DATOS PARA LAS METRICAS
    df_actual = df.drop_duplicates(subset=["ciudad"], keep="first")

    st.subheader("?? Estado Actual en las Regiones Monitoreadas")
    columnas_metricas = st.columns(len(df_actual))

    for i, fila in enumerate(df_actual.to_dict(orient="records")):
        with columnas_metricas[i]:
            st.metric(
                label = fila["ciudad"],
                value = f"{fila['temperatura_c']} Grados Centigrados",
                delta = fila["estado_clima"]
            )
    st.write("---------------------")        

    # 5 GRAFICOS INTERACTIVOS
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"?? Evolucion de la Temperatura en {ciudad_seleccionada}")
        if not df_ciudad.empty:
            fig_linea = px.line(
                df_ciudad,
                x = "fecha_extraccion",
                y = "temperatura_c",
                labels = {"fecha_extraccion": "Fechas y Hora", "tempratura_c": "Temperatura (Grados Centigrados)"},
                markers = True,
                template = "plotly_dark"
            )
            st.plotly_chart(fig_linea, use_container_width = True)
        else:
            st.info("No hay suficientes datos historicos para esta ciudad.")

    with col2:
        st.subheader("?? Comparativa de Humedad Actual")
        fig_barra = px.bar(
            df_actual,
            x = "ciudad",
            y = "humedad_porcentaje",
            color = "ciudad",
            labels = {"ciudad": "Ciudad", "humedad_porcentaje": "Humedad (%)"},
            template = "plotly_dark"
        )
        st.plotly_chart(fig_barra, use_container_width = True)

except Exception as e:
    st.error(f"Error al conectar con el Dashboard: {e}")