import streamlit as st
import pandas as pd
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar el tokenizador y el modelo DistilBERT
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english", clean_up_tokenization_spaces=True)
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

# Función para analizar la polaridad de los comentarios
def polaridad(comentario):
    global tokenizer, model

    # Tokenizar el comentario con truncamiento para evitar secuencias largas
    inputs = tokenizer(comentario, return_tensors="pt", truncation=True, max_length=512)

    # Obtener las predicciones
    with torch.no_grad():
        logits = model(**inputs).logits

    # Obtener la etiqueta predicha
    predicted_class_id = logits.argmax().item()
    return model.config.id2label[predicted_class_id]

# Interfaz de Streamlit
st.title("Análisis de Sentimiento con DistilBERT")

# Subir archivo CSV con comentarios
uploaded_file = st.file_uploader("Sube un archivo CSV con comentarios", type=["csv"])

# Si se ha subido el archivo, se muestra la tabla
if uploaded_file is not None:
    # Leer el archivo CSV
    df = pd.read_csv(uploaded_file, sep=";")
    
    # Verificar si la columna 'review' está en el archivo
    if 'review' in df.columns and 'polaridad' in df.columns:
        # Mostrar la tabla previa
        st.write("Vista previa de los datos:")
        st.dataframe(df)

        # Agregar un botón para aplicar el análisis de sentimiento
        if st.button("Aplicar Análisis de Sentimiento"):
            # Aplicar la función de polaridad a la columna de comentarios
            df['polaridad_bert'] = df['review'].apply(lambda x: polaridad(x))

            # Convertir 'polaridad_bert' a valores numéricos
            df['polaridad_bert_num'] = df['polaridad_bert'].apply(lambda x: 1 if x == "POSITIVE" else 0)

            # Mostrar los resultados
            st.subheader("Resultados del Análisis de Sentimiento")
            st.dataframe(df[['review', 'polaridad', 'polaridad_bert']])

            # Generar la matriz de confusión
            st.subheader("Matriz de Confusión")
            cm = confusion_matrix(df['polaridad'], df['polaridad_bert_num'])

            # Visualizar la matriz de confusión usando Seaborn
            fig, ax = plt.subplots()
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["NEGATIVE", "POSITIVE"], yticklabels=["NEGATIVE", "POSITIVE"])
            plt.xlabel("Predicción (BERT)")
            plt.ylabel("Valor Real")
            plt.title("Matriz de Confusión entre polaridad y polaridad_bert")

            # Mostrar la matriz de confusión en Streamlit
            st.pyplot(fig)

            # Opción para descargar los resultados
            st.subheader("Descargar resultados")
            csv = df.to_csv(index=False, sep=";").encode('utf-8')
            st.download_button(label="Descargar CSV con resultados",
                               data=csv,
                               file_name="resultados_sentimiento.csv",
                               mime='text/csv')

    else:
        st.error("El archivo CSV no contiene las columnas necesarias ('review' y 'polaridad'). Asegúrate de que los comentarios y polaridades estén en las columnas correctas.")

else:
    st.info("Por favor, sube un archivo CSV con una columna de comentarios llamada 'review' y una columna de polaridad.")
