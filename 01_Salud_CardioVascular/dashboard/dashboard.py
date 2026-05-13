# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os

#----------- CONFIGURACION DE PAGINA
st.set_page_config(
    page_title="Dashboard Salud Cardiovascular",
    page_icon="❤️",
    layout="wide"
)

# ------------- CARGAR DATOS DESDE SQL ---------------
# CONECTAMOS DIRECTAMENTE A LA BASE DE DATOS QUE GENERO EL ETL
ruta_db = os.path.join(os.path.dirname(__file__), "../data/salud.db")
conexion = sqlite3.connect(ruta_db)

# read_sql() - LEE TODA LA TABLA PACIENTES EN U NDATAFRAME
df = pd.read_sql("SELECT * FROM pacientes", conexion)
conexion.close()

print(f"Datos cargados: {df.shape}")

# --------- TITULO ----------------
st.title("❤️ Dashboard - Salud Cardiovascular")
st.markdown("Analisis de factores de riesgo en enfermedades cardiacas")
st.markdown("-------")

#----- SECCION 1 - KPIs PRINCIPALES ---------
st.subheader("📊 Indicadores Principales")

#CALCULAMOS LAS METRICAS
total_pacientes = len(df)
con_enfermedad = len(df[df["enfermedad_cardiaca"] == "Si"])
#len() -  CUENTA LAS FILAS QUE CUMPLEN LA CONDICION

porcentaje_enfermedad = (con_enfermedad / total_pacientes) * 100

edad_promedio = df["edad"].mean()
colesterol_promedio = df["colesterol"].mean()

#MOSTRAMOS LAS 4 METRICAS EN COLUMNAS 
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label= "👥 Total Pacientes",
        value= total_pacientes
    )

with col2:
    st.metric(
        label = "❤️ Con Enfermedad",
        value = f"{con_enfermedad} ({porcentaje_enfermedad:.1f}%)"
        # :.1f - MUESTRA SOLO 1 DECIMAL
    )
    
with col3:
    st.metric(
        label = "📅 Edad Promedio",
        value = f"{edad_promedio:.1f} a?os"
    )

with col4:
    st.metric(
        label = "🩸 Colesterol Promedio",
        value = f"{colesterol_promedio:.1f} mg/dl"
    )

st.markdown("************")

# ---- SECCION 2 - FILTROS INTERACTIVOS
st.subheader("?? Filtros")

# DIVIDIMOS EN 2 COLUMNAS PARA LOS FILTROS
col1, col2 = st.columns(2)

with col1:
    #st.selectbox() - MENU DESPLEGABLE CON OPCIONES
    sexo_filtro = st.selectbox(
        "Filtrar por Sexo",
        options=["Todos"] + list(df["sexo"].unique())
        # ["Todos"] + list() - agrega "Todos" como primera opcion
    )

with col2:
    # st.multiselect() - seleccion multiple
    edad_filtro = st.multiselect(
        "Filtrar por Grupo de Edades:",
        options = df["grupo_edad"].unique(),
        default = df["grupo_edad"].unique()
    )

# APLICAR FILTROS AL DATAFRAME
df_filtrado = df.copy()
#copy() CREA UNA COPIA DEL DATAFRAME ARA NO MODIFICAR EL ORIGINAL

if sexo_filtro != "Todos":
    df_filtrado = df_filtrado[df_filtrado["sexo"] == sexo_filtrado]

if edad_filtro:
    df_filtrado = df_filtrado[df_filtrado["grupo_edad"].isin(edad_filtro)]
    #isin() - FILTRA LOS VALORES QUE ESTEN EN LA LISTA SELECCIONADA

# actualizar metricas con los filtros aplicados
st.markdown(f"****Pacientes filtrados: {len(df_filtrado)}****")
st.markdown("-----------")

# SECCION 3 - GRAFICAS
st.subheader("?? Analisis Visual")

col1, col2 = st.columns(2)

with col1:
    # Grafica - Distribucion por sexo
    st.markdown("**Distribucion por Sexo**")
    por_sexo = df_filtrado.groupby(["sexo", "enfermedad_cardiaca"]).size()
    # size() - cuenta los registros de cada grupo
    por_sexo = por_sexo.unstack()
    # unstack() - convierte el segundo nivel del indice en columnas
    fig, ax = plt.subplots()
    por_sexo.plot(kind="bar", ax=ax, color=["lightblue", "salmon"])
    # color=[] - colores para cada barra
    ax.set_xlabel("Sexo")
    ax.set_ylabel("Total Pacientes")
    ax.legend(["Sin Enfermedad", "Con Enfermedad"])
    # legend() - agrega la leyenda con los nombres
    ax.tick_params(axis="x", rotation=0)
    st.pyplot(fig)
    plt.close()
    # plt.close() - cierra la figura para liberar memoria

with col2:
    # Grafica - Distribucion por grupo de edad
    st.markdown("**Distribucion por Grupo de Edad**")
    por_edad = df_filtrado.groupby(["grupo_edad", "enfermedad_cardiaca"]).size()
    por_edad = por_edad.unstack()
    fig2, ax2 = plt.subplots()
    por_edad.plot(kind="bar", ax=ax2, color=["lightblue", "salmon"])
    ax2.set_xlabel("Grupo de Edad")
    ax2.set_ylabel("Total Pacientes")
    ax2.legend(["Sin Enfermedad", "Con Enfermedad"])
    ax2.tick_params(axis="x", rotation=45)
    st.pyplot(fig2)
    plt.close()

st.markdown("---")

# ---- SECCION 4 - FACTORES DE RIESGO ----
st.subheader("?? Factores de Riesgo")

col1, col2 = st.columns(2)

with col1:
    # Grafica - Colesterol promedio por enfermedad
    st.markdown("**Colesterol Promedio**")
    colesterol_enfermedad = df_filtrado.groupby("enfermedad_cardiaca")["colesterol"].mean()
    fig3, ax3 = plt.subplots()
    colesterol_enfermedad.plot(kind="bar", ax=ax3, color=["lightblue", "salmon"])
    ax3.set_xlabel("Tiene Enfermedad")
    ax3.set_ylabel("Colesterol Promedio (mg/dl)")
    ax3.tick_params(axis="x", rotation=0)
    st.pyplot(fig3)
    plt.close()

with col2:
    # Grafica - Frecuencia cardiaca maxima por enfermedad
    st.markdown("**Frecuencia Cardiaca Maxima**")
    frec_enfermedad = df_filtrado.groupby("enfermedad_cardiaca")["frec_cardiaca_max"].mean()
    fig4, ax4 = plt.subplots()
    frec_enfermedad.plot(kind="bar", ax=ax4, color=["lightblue", "salmon"])
    ax4.set_xlabel("Tiene Enfermedad")
    ax4.set_ylabel("Frecuencia Cardiaca Maxima")
    ax4.tick_params(axis="x", rotation=0)
    st.pyplot(fig4)
    plt.close()

st.markdown("---")

# ---- SECCION 5 - TABLA INTERACTIVA ----
st.subheader("?? Datos Detallados")
st.dataframe(df_filtrado[[
    "edad", "sexo", "grupo_edad", "colesterol",
    "nivel_colesterol", "presion_arterial",
    "frec_cardiaca_max", "enfermedad_cardiaca"
]])

# ---- SECCION 6 - DESCARGA ----
st.subheader("?? Descargar Datos")
import io
buffer = io.BytesIO()

with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    df_filtrado.to_excel(writer, sheet_name="Pacientes", index=False)
    df_filtrado.groupby("grupo_edad")["enfermedad_cardiaca"]\
        .value_counts().reset_index()\
        .to_excel(writer, sheet_name="Por Edad", index=False)
    df_filtrado.groupby("sexo")["enfermedad_cardiaca"]\
        .value_counts().reset_index()\
        .to_excel(writer, sheet_name="Por Sexo", index=False)

st.download_button(
    label="?? Descargar Reporte Excel",
    data=buffer.getvalue(),
    file_name="reporte_salud.xlsx",
    mime="application/vnd.ms-excel"
)