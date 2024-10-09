import streamlit as st
import altair as alt
import pandas as pd

df = pd.read_csv("../Datos/quality_life_2020.csv", sep=";")

###################################
# Gráfica de caja y bigotes
##################################

# Selecciona la variabe a desplegar:
# Crear un selector en la barra lateral para elegir la variable numérica a visualizar
variables_numericas = df.select_dtypes(include=['float64', 'int64']).columns.tolist()  # Filtrar solo las variables numéricas
variable_seleccionada = st.sidebar.selectbox("Selecciona la variable para la gráfica de caja", variables_numericas)

st.subheader("Gráfico de caja y bigotes")

st.write(variable_seleccionada)

box_plot = alt.Chart(df).mark_boxplot().encode(
    y=alt.Y(f'{variable_seleccionada}:Q', title=f'{variable_seleccionada}', scale=alt.Scale(zero=False))  # Eje Y numérico para el índice
).properties(
    width=600,
    height=400
)

st.altair_chart(box_plot, use_container_width=True)

