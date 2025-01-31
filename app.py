import streamlit as st
from analysis import analyze_text
from generate import generate_infographic
import docx

def read_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

st.set_page_config(page_title="Infographic Generator", layout="wide")

st.title("📊 Генератор инфографики из текста")

text_input = st.text_area("Введите текст или загрузите файл:", height=200)
uploaded_file = st.file_uploader("", type=["txt", "docx"])

if uploaded_file:
    if uploaded_file.type == "text/plain":
        text_input = uploaded_file.read().decode()
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text_input = read_docx(uploaded_file)

if st.button("Сгенерировать инфографику"):
    if text_input:
        with st.spinner("Анализируем текст..."):
            lang = "ru" if any(cyr_char in text_input for cyr_char in "абвгдеёжзий") else "en"
            analysis = analyze_text(text_input[:1000], lang=lang)
        
        with st.spinner("Создаём инфографику..."):
            output = generate_infographic(analysis)
        
        st.image(output)
        with open(output, "rb") as f:
            st.download_button("Скачать PNG", f, file_name="infographic.png")
    else:
        st.warning("Пожалуйста, введите текст или загрузите файл")
