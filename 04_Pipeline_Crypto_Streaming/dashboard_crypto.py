# -*- coding: utf-8 -*-
import os
import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine
from dotenv import load_dotenv

# 1 CONFIGURACION DE LA PAGINA DE STREAMLIT
st.set_page_config(page_title="Crypto Ticker Dashboard", page_icon="??", layout="wide")

# 2 CARGAR CREDENCIALES SEGURAS (.env)
carpeta_actual = os.path.dirname(__file__)
ruta_env = os.path.join(carpeta_actual, "..", ".env")
load_dotenv(dotenv_path=ruta_env)

USUARIO = os.getenv("DB_USER")
CLAVE = os.getenv("DB_PASSWORD")
SERVIDOR = os.getenv("DB_HOST")
PUERTO = os.getenv("DB_PORT")
BASE_DATOS = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{USUARIO}:{CLAVE}@{SERVIDOR}:{PUERTO}/{BASE_DATOS}"

@st.cache_data(ttl=30) # CACHE DE 30 SEGUNDOS PARA DATOS FINANCIEROS VOLATILES
def cargar_datos_crypto():
    engine = create_engine(DATABASE_URL)
    query = "SELECT * FROM crypto_historico ORDER BY ultima_actualizacion DESC"
    df = pd.read_sql(query, con=engine)
    df["ultima_actualizacion"] = pd.to_datetime(df["ultima_actualizacion"])
    return df

try:
    df = cargar_datos_crypto()

    # TITULO PRINCIPAL
    st.title("PANEL DE MONITOREO DE CRIPTOMONEDAS EN VIVO")
    st.markdown("Analisis de precios en tiempo real para activos financieros con almacenamiento en Supabase Cloud")
    st.write("----------------------------------------")

    # 3 FILTROS EN LA BARRA LATERAL
    st.sidebar.header("Filtros de Mercado")
    activos_disponibles = df["activo_id"].unique()
    activo_seleccionado = st.sidebar.selectbox("Selecciona un activo para ver su detalle:", activos_disponibles)

    # FILTRAR DATOS POR EL ACTIVO SELECCIONADO PARA LOS GRAFICOS HISTORICOS
    df_activo = df[df["activo_id"] == activo_seleccionado].sort_values("ultima_actualizacion")

    # TOMAR LA ULTIMA FOTO DEL MERCADO (EL REGISTRO MAS RECIENTE DE CADA MONEDA)
    df_actual = df.drop_duplicates(subset=["activo_id"], keep="first")

    # 4 TARJETAS DE METRICAS CON SU ESTADO ACTUAL
    st.subheader("COTIZACIONES ACTUALES DEL MERCADO")
    columnas_metricas = st.columns(len(df_actual))

    for i, fila in enumerate(df_actual.to_dict(orient="records")):
        with columnas_metricas[i]:
            # SE FORMATEAN LOS NUMEROS PARA QUE SE VEAN COMO DINERO REAL
            precio_usd_formateado = f"${fila['precio_usd']:,.2f} USD"
            st.metric(
                label=fila["activo_id"],
                value=precio_usd_formateado,
                delta=f"${fila['precio_cop']:,.0f} COP"
            )
            
    st.write("-------------------------------------")

    

    # 5 GRAFICOS INTERACTIVOS (PLOTLY) - FUERA DEL BUCLE FOR
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Historico de Precio USD - {activo_seleccionado}")
        if not df_activo.empty:
            fig_usd = px.line(
                df_activo,
                x="ultima_actualizacion",
                y="precio_usd",
                labels={"ultima_actualizacion": "Fecha y Hora", "precio_usd": "Precio (USD)"},
                markers=True,
                template="plotly_dark"
            )
            # Personalizamos el color de la linea para que parezca un terminal financiero
            fig_usd.update_traces(line_color="#00FFCC")
            st.plotly_chart(fig_usd, use_container_width=True)
        else:
            st.info("Esperando mas capturas del robot para graficar la tendencia.")

    with col2:
        st.subheader(f"Historico de Precio COP - {activo_seleccionado}")
        if not df_activo.empty:
            fig_cop = px.line(
                df_activo,
                x="ultima_actualizacion",
                y="precio_cop",
                labels={"ultima_actualizacion": "Fecha y Hora", "precio_cop": "Precio (COP)"},
                markers=True,
                template="plotly_dark"
            )
            fig_cop.update_traces(line_color="#FF9900")
            st.plotly_chart(fig_cop, use_container_width=True)
        else:
            st.info("Esperando mas capturas del robot para graficar la tendencia.")

except Exception as e:
    st.error(f"Error al conectar con el Dashboard Financiero: {e}")