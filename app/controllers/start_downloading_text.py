from controllers.scrap_write_text import scrap_write_text
from controllers.scrap_clean_text import scrap_clean_text
from controllers.scrap_text import scrap_text
import os

def start_downloading_text(file_name):
    
    current_dir = os.path.dirname(__file__)
    links_path = os.path.join(current_dir, "..", "links")
    file_path = os.path.join(links_path, file_name)
    
    try:
        with open(file_path, 'r') as f:
            links = [line.strip() for line in f.readlines()]
            
        for link in links:
            print(f"Procesando URL: {link}")
            text = scrap_text(link)
            print(f"Texto obtenido: {text}")
            # clean_text = scrap_clean_text(text)
            # print(f"Texto limpio: {clean_text}")
            scrap_write_text(text, link)
    except Exception as e:
        print(f"Error al escribir texto: {e}")