import spacy
from transformers import pipeline

nlp_ru = spacy.load("ru_core_news_sm")
nlp_en = spacy.load("en_core_web_sm")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def analyze_text(text, lang="ru"):
    doc = nlp_ru(text) if lang == "ru" else nlp_en(text)
    
    headers = [sent.text for sent in doc.sents if any(token.pos_ in ["NOUN", "PROPN"] for token in sent)]
    
    facts = []
    numbers = []
    for ent in doc.ents:
        if ent.label_ in ["DATE", "CARDINAL", "PERCENT"]:
            facts.append(ent.text)
            if ent.label_ == "CARDINAL":
                try:
                    numbers.append(float(ent.text))
                except:
                    pass

    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    key_points = summary[0]["summary_text"].split(". ")

    return {
        "headers": headers[:3],
        "facts": facts[:5],
        "numbers": numbers,
        "key_points": key_points
    }
