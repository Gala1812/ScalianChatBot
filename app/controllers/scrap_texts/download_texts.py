from controllers.scrap_texts.save_texts import save_texts
from controllers.scrap_texts.clean_text import clean_text
from controllers.scrap_texts.get_text import get_text
import os

def download_texts(file_name):
    """ Download and process texts from a file containing URLs.
    Args:
        file_name (str): The name of the file containing the URLs.
    Returns:
        None
    Examples:
        >>> download_texts("url_list.txt")
        Procesando URL: https://www.example.com
        Procesando URL: https://www.example.com/page1
        Procesando URL: https://www.example.com/page2
    """
    
    current_dir = os.path.dirname(__file__)
    links_path = os.path.join(current_dir, "../..", "links")
    file_path = os.path.join(links_path, file_name)
    
    try:
        with open(file_path, 'r') as f:
            links = [line.strip() for line in f.readlines()]
            
        for link in links:
            print(f"Procesando URL: {link}")
            title, text = get_text(link)
            save_texts(title, text, link)
    except Exception as e:
        print(f"Error al escribir texto: {e}")