import os
from urllib.parse import urlparse
from controllers.scrap_texts.clean_text import clean_text

def clean_filename(url):
    parsed_url = urlparse(url)
    host_name = parsed_url.netloc.replace(".", "_")
    path_segments = parsed_url.path.strip("/").split("/")
    path_name = "_".join(path_segments)

    return f"{host_name}_{path_name}"

def save_texts(text, url):
    current_dir = os.path.dirname(__file__)
    texts_path = os.path.join(current_dir, "../..", "texts")

    clean_url = clean_filename(url)
    file_path = os.path.join(texts_path, f"{clean_url}.txt")
    
    if not os.path.exists(texts_path):
        os.makedirs(texts_path)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        clean_text(file_path)
        print(f"Texto escrito en texts/{clean_url}.txt\n")
    except Exception as e:
        print(f"Error al escribir texto: {e}")