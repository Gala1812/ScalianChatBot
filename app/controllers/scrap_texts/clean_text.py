import re

def clean_text(text):
    text = re.sub(r'[\t]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    return text.strip()