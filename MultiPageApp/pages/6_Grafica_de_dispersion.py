import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

df = pd.read_csv("../Datos/quality_life_2020.csv", sep=";")

###################################
# Gráfica de dispersión
##################################

# Gráfica de dispersión

# Agregar un dropdown para seleccionar las variables a visualizar

variables_numericas = df.select_dtypes(include=['float64', 'int64']).columns.tolist()  # Filtrar solo las variables numéricas
var_1 = st.sidebar.selectbox("Selecciona variable 1 (horizontal)", variables_numericas)
var_2 = st.sidebar.selectbox("Selecciona variable 2 (vertical)", variables_numericas)

st.subheader("Gráfica de dispersión")
scatter_chart = alt.Chart(df).mark_circle().encode(
    x = alt.X(var_1, scale=alt.Scale(zero=False)),
    y = alt.Y(var_2, scale=alt.Scale(zero=False)),
    tooltip = ['Country', var_1, var_2]
)

st.altair_chart(scatter_chart, use_container_width=True)

st.write(f'Correlación entre {var_1} y {var_2}: {np.round(df[var_1].corr(df[var_2]), 2)}')
