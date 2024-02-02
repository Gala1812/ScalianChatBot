import os

def clean_filename(url):
    # Mantener solo caracteres alfanuméricos y algunos caracteres especiales
    return "".join(c for c in url if c.isalnum() or c in ('.', '_', '-'))

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
        print(f"Texto escrito en texts/{clean_url}.txt")
    except Exception as e:
        print(f"Error al escribir texto: {e}")