import os
from controllers.scrap_texts.clean_text import clean_text
from controllers.scrap_texts.clean_filename import clean_filename
from controllers.scrap_texts.remove_header_sspain import remove_header_sspain
from controllers.scrap_texts.remove_footer_sspain import remove_footer_sspain


def save_texts(text, url):
    current_dir = os.path.dirname(__file__)
    texts_path = os.path.join(current_dir, "../..", "texts")

    clean_url = clean_filename(url)
    file_path = os.path.join(texts_path, f"{clean_url}.txt")

    if not os.path.exists(texts_path):
        os.makedirs(texts_path)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        clean_text(file_path)
        remove_header_sspain(file_path)
        remove_footer_sspain(file_path)
        print(f"Texto escrito en texts/{clean_url}.txt\n")
    except Exception as e:
        print(f"Error al escribir texto: {e}")
