import streamlit as st
import pandas as pd
from textblob import TextBlob
import re
from googletrans import Translator

# Configuración de la página
st.set_page_config(
    page_title="🎉 Analizador de Texto Divertido",
    page_icon="🤖",
    layout="wide"
)

# Estilos personalizados y dinámicos
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #fff0f5, #f0fff0);
    }
    .main {
        color: #333333;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    h1, h2, h3 {
        color: #ff69b4;
        text-shadow: 1px 1px #fff;
    }
    .stButton > button {
        background-image: linear-gradient(to right, #ff7eb3, #ff758c);
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 18px;
        padding: 10px 20px;
        transition: 0.3s ease;
    }
    .stButton > button:hover {
        background-image: linear-gradient(to right, #fcb69f, #ffecd2);
        color: #333;
        transform: scale(1.05);
    }
    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Imagen decorativa en la parte superior
st.image("https://i.imgur.com/0XjzXkY.png", width=800, caption="✨ ¡Analiza tus textos con estilo! ✨")

# Título principal
st.title("📝 Analizador de Texto con TextBlob 🕵️‍♀️")

# Descripción
st.markdown("""
¡Bienvenido! 🎈 Esta app analiza tu texto con un toque de diversión:

- 🔍 Sentimiento y subjetividad
- 🗝️ Palabras clave
- 📊 Frecuencia de palabras

¡Todo esto con color, imágenes y emojis! 🎨✨
""")

# Barra lateral
st.sidebar.title("🎛️ Opciones mágicas")
modo = st.sidebar.radio(
    "¿Cómo quieres ingresar tu texto?",
    ["🖊️ Escribir texto", "📁 Subir archivo"]
)

# Funciones auxiliares
def contar_palabras(texto):
    palabras = re.findall(r'\b\w+\b', texto.lower())
    return pd.Series(palabras).value_counts()

def traducir_texto(texto):
    traductor = Translator()
    return traductor.translate(texto, src='es', dest='en').text

def procesar_texto(texto):
    blob = TextBlob(texto)
    traduccion = traducir_texto(texto)
    frases = [{"original": str(frase), "traducido": traducir_texto(str(frase))} for frase in blob.sentences]
    return {
        "texto_original": texto,
        "texto_traducido": traduccion,
        "sentimiento": blob.sentiment.polarity,
        "subjetividad": blob.sentiment.subjectivity,
        "contador_palabras": contar_palabras(texto),
        "frases": frases
    }

# Función para visualizaciones
def crear_visualizaciones(resultados):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Sentimiento y Subjetividad")
        sentimiento_norm = (resultados["sentimiento"] + 1) / 2
        st.progress(sentimiento_norm)
        st.success(f"Sentimiento: {resultados['sentimiento']:.2f}")
        st.progress(resultados["subjetividad"])
        st.info(f"Subjetividad: {resultados['subjetividad']:.2f}")

    with col2:
        st.subheader("🔠 Top palabras")
        top_words = dict(list(resultados["contador_palabras"].items())[:10])
        st.bar_chart(top_words)

    st.subheader("🌍 Traducción del texto")
    with st.expander("👀 Ver traducción"):
        col1, col2 = st.columns(2)
        col1.text_area("Texto original", resultados["texto_original"], height=200)
        col2.text_area("Texto traducido", resultados["texto_traducido"], height=200)

    st.subheader("🧩 Frases detectadas")
    for i, frase in enumerate(resultados["frases"][:10]):
        blob = TextBlob(frase['traducido'])
        s = blob.sentiment.polarity
        emoji = "😊" if s > 0.05 else "😐" if s >= -0.05 else "😞"
        st.markdown(f"{i+1}. {emoji} **Original**: '{frase['original']}'")
        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;**Traducción**: '{frase['traducido']}' (Sentimiento: {s:.2f})")
        st.markdown("---")

# Modo de entrada
if modo == "🖊️ Escribir texto":
    texto = st.text_area("Escribe tu texto aquí 🧠", height=200, placeholder="Había una vez una historia increíble...")
    if st.button("🔍 Analizar texto"):
        if texto.strip():
            with st.spinner("✨ Procesando magia analítica..."):
                resultados = procesar_texto(texto)
                crear_visualizaciones(resultados)
        else:
            st.warning("🚨 ¡No olvides ingresar texto primero!")

elif modo == "📁 Subir archivo":
    archivo = st.file_uploader("📂 Sube tu archivo de texto:", type=["txt", "csv", "md"])
    if archivo:
        try:
            contenido = archivo.getvalue().decode("utf-8")
            st.text_area("📄 Contenido", contenido[:1000])
            if st.button("📊 Analizar archivo"):
                with st.spinner("🧙‍♀️ Analizando..."):
                    resultados = procesar_texto(contenido)
                    crear_visualizaciones(resultados)
        except Exception as e:
            st.error(f"⚠️ Error: {e}")

# Pie de página
st.markdown("""
---
<center>✨ Creado con ❤️ por Cami para hacer el análisis textual más colorido y entretenido 🚀</center>
""", unsafe_allow_html=True)

