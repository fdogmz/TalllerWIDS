from langchain_core.messages import AIMessage
from langchain_ollama import ChatOllama
import streamlit as st

connected = False

try:
    # Conectar al modelo de Ollama
    llm = ChatOllama(
        model="llama3.2",
        temperature=0
    )

    connected = True

    st.header("Solución del problema matemático con Ollama")

    # Función para obtener la respuesta del modelo de Ollama
    def resolver_problema(problema_matematico):
        prompt = f"Resuelve el siguiente problema matemático paso a paso:\n\n{problema_matematico}"
        
        try:
            messages = [
                (
                    "system",
                    "Eres un asistente útil que resuelve problemas matemáticos. Resuelve el problema planteado por el usuario",
                ),
                ("human", problema_matematico),
            ]
            ai_msg = llm.invoke(messages)

            return f"**Ollama**: {ai_msg.content}"            
        except Exception as e:
            return f"Error al obtener respuesta: {e}"

except:
    st.sidebar.warning("Error al cargar el modelo de Ollama. Por favor, revisa la configuración.")

if connected:
    st.sidebar.title("Asistente Matemático con Ollama")

    # Mover las instrucciones y entrada del problema matemático a la barra lateral
    st.sidebar.write("¡Hola! Soy Ollama, un asistente virtual que te ayudará a resolver problemas matemáticos.")
    st.sidebar.write("Plantea un problema matemático y yo lo resolveré.")

    # Entrada del problema matemático en la barra lateral
    problema_matematico = st.sidebar.text_area("Introduce tu problema matemático aquí:")

    # Mostrar el botón para resolver el problema siempre
    if st.sidebar.button("Resolver"):
        if problema_matematico:
            # Obtener la respuesta del asistente de matemáticas
            respuesta = resolver_problema(problema_matematico)
            
            # Mostrar la respuesta en la página principal
            st.write("### Respuesta del Asistente:")
            st.write(respuesta)
        else:
            st.warning("Por favor, introduce un problema matemático antes de presionar 'Resolver'.")
