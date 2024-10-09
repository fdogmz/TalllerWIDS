import streamlit as st
import pandas as pd
import altair as alt

# En esta app exploraremos varios componentes que permiten visualizar datos e información en una aplicación

st.title("Calidad de vida a nivel mundial")

###################################
# markdown
##################################

st.subheader("Indicadores")
st.markdown("""
            En esta aplicación exploraremos la distribución de diferentes indicadores que nos permiten medir la calidad de vida en diferentes países.  
            Exploraremos los siguientes:
            * Índice de calidad de vida.
            * Índice de poder de compra.
            * Índice de seguridad.
            * Índice de salud.
            * Índice de costo de vida.
            * Razón de precios de la propiedad.
            * Índice de tiempo de desplazamiento.
            * Índice de contaminación.
            * Índice climático.
            """)

###################################
# Tabla de datos
##################################


st.subheader("Tabla de datos")
st.write("Los datos que exploraremos están disponibles en la siguiente tabla:")

df = pd.read_csv("../Datos/quality_life_2020.csv", sep=";")
#df = df.reset_index(drop=True)
st.dataframe(df)

###################################
# Gráfico de barras
##################################

st.subheader("Gráfica de barras")

# Agregar un switch que cambie entre los 10 primeros o los últimos 10

# gráfica de barras con el índice de calidad de vida de los 10 primeros países
df_bar = df[['Country', 'Quality of Life Index']].iloc[:10].sort_values(by='Quality of Life Index', ascending=False)

# Crear gráfico de barras usando Altair
chart = alt.Chart(df_bar).mark_bar().encode(
    x=alt.X('Country', sort=None),  # Eje X con nombres de los países
    y='Quality of Life Index'  # Eje Y con los valores numéricos
).properties(
    width=600,  # Ajustar el tamaño del gráfico
    height=400
)


# Mostrar el gráfico en Streamlit
st.altair_chart(chart, use_container_width=True)

###################################
# Histograma de frecuencias
##################################

st.subheader("Histograma de frecuencias")

# Agregar un selector de enteros para elegir el número de bines

histogram = alt.Chart(df).mark_bar().encode(
    x=alt.X('Quality of Life Index', bin=True),
    y='count()',
    tooltip='count()'
).properties(
    width=600,
    height=400
)

st.altair_chart(histogram, use_container_width=True)

###################################
# Gráfica de caja y bigotes
##################################

st.subheader("Gráfico de caja y bigotes")

box_plot = alt.Chart(df).mark_boxplot().encode(
    y=alt.Y('Quality of Life Index:Q', title='Quality of Life Index', scale=alt.Scale(zero=False))  # Eje Y numérico para el índice
).properties(
    width=600,
    height=400
)

st.altair_chart(box_plot, use_container_width=True)

###################################
# Gráfica de dispersión
##################################

# Gráfica de dispersión

# Agregar un dropdown para seleccionar las variables a visualizar

st.subheader("Gráfica de dispersión")
scatter_chart = alt.Chart(df).mark_circle().encode(
    x = alt.X('Quality of Life Index', scale=alt.Scale(zero=False)),
    y = alt.Y('Pollution Index', scale=alt.Scale(zero=False)),
    tooltip = ['Country', 'Quality of Life Index', 'Safety Index']
)

st.altair_chart(scatter_chart, use_container_width=True)
