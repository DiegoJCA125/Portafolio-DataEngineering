import streamlit as st
import pandas as pd
import sqlite3
import os
import plotly.express as px

# CONFIGURACION DE LA PAGINA 
st.set_page_config(page_title = "E-commerce Analytics", layout = "wide")

# RUTAS
ruta_script = os.path.dirname(__file__)
ruta_db = os.path.join(ruta_script, "..", "database", "ecommerce_sales.db")

# CONEXION Y CARGA
def cargar_datos():
    if os.path.exists(ruta_db):
        conn = sqlite3.connect(ruta_db)
        df = pd.read_sql("SELECT * FROM ventas_procesadas", conn)
        conn.close()
        return df
    return None

df = cargar_datos()

if df is not None:
    st.title(" Dashboard de Ingenieria de Ventas")
    st.markdown("--------------")

    # ------ SIDEBAR (FILTROS) ------
    st.sidebar.header("Filtros del Proyecto")
    lista_paises = st.sidebar.multiselect(
        "Selecciona Paises:",
        options = df["pais"].unique(),
        default = df["pais"].unique()[:3]
    )

    # --------- FILTRAR DATOS
    df_filtrado = df[df["pais"].isin(lista_paises)]

    #---- KPIs (METRICAS PRINCIPALES)
    col1, col2, col3 = st.columns(3)
    with col1:
        total_vendas = df_filtrado["ingreso_total"].sum()
        st.metric("Ingresos Totales", f"$ {total_vendas:,.2f}")
    with col2:
        ticket_promedio = df_filtrado["ingreso_total"].mean()
        st.metric("Ticket Promedio", f"$ {ticket_promedio:.2f}")
    with col3:
        num_clientes = df_filtrado["id_cliente"].nunique()
        st.metric("Clientes Unicos", num_clientes)
    
    st.markdown("--------------------")

    # ---------------------- GRAFICOS ----------
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Top 10 Productos por Ingreso")
        # SE USA PLOTLY PARA QUE EL GRAFICO SEA INTERACTIVO
        fig_prod = px.bar(
            df_filtrado.groupby("descripcion")["ingreso_total"].sum().sort_values(ascending = False).head(10),
            orientation = 'h',
            color_continuous_scale = "Viridis"
        )
        st.plotly_chart(fig_prod, width = 'stretch')

    with c2:
        st.subheader("Distribucion de Ventas por Pais")
        fig_pie = px.pie(df_filtrado, values = 'ingreso_total', names = 'pais')
        st.plotly_chart(fig_pie, use_container_width= True)

else:
    st.error("No se encontro la base de datos. Ejecute primero el ETL")