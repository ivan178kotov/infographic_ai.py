import spacy
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from transformers import pipeline

# Загрузка NLP-модели
nlp = spacy.load("ru_core_news_sm")

# Инициализация ИИ для генерации текста (GPT-2)
text_generator = pipeline("text-generation", model="gpt2")

def analyze_text(text):
    """Анализ текста и извлечение ключевых данных"""
    doc = nlp(text)
    
    # Извлечение сущностей
    entities = {ent.text: ent.label_ for ent in doc.ents}
    
    # Извлечение ключевых слов (первые 5 существительных)
    keywords = [token.text for token in doc if token.pos_ == "NOUN"][:5]
    
    return {
        "keywords": keywords,
        "entities": entities,
        "sentences": [sent.text for sent in doc.sents][:3]  # первые 3 предложения
    }

def create_infographic(data):
    """Генерация инфографики"""
    # Создание фона
    img = Image.new("RGB", (800, 1200), color="white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    
    # Заголовок
    draw.text((50, 50), "Инфографика по тексту:", font=font, fill="black")
    
    # Ключевые слова
    y = 150
    draw.text((50, y), "Ключевые слова:", font=font, fill="blue")
    for word in data["keywords"]:
        y += 40
        draw.text((70, y), f"- {word}", font=font, fill="black")
    
    # График (пример)
    plt.figure(figsize=(4, 2))
    plt.bar(range(len(data["keywords"])), [10]*len(data["keywords"]))
    plt.savefig("temp_plot.png")
    img.paste(Image.open("temp_plot.png"), (50, 400))
    
    # Сохранение
    img.save("infographic.png")
    return img

# Веб-интерфейс
st.title("🖼️ ИИ-помощник для инфографики")
text_input = st.text_area("Введите текст:", height=200)

if st.button("Создать инфографику"):
    if text_input:
        data = analyze_text(text_input)
        infographic = create_infographic(data)
        st.image(infographic, caption="Сгенерированная инфографика")
        st.download_button(
            label="Скачать",
            data=open("infographic.png", "rb").read(),
            file_name="infographic.png",
            mime="image/png"
        )
    else:
        st.error("Введите текст!")
