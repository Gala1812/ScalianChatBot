import os
from controllers.scrap_texts.save_texts import save_texts
from controllers.scrap_texts.clean_text import clean_text
from controllers.scrap_texts.get_text import get_text
from controllers.scrap_texts.counter import counter

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
    texts_path = os.path.join(current_dir, "../..", "texts")
    
    try:
        with open(file_path, 'r') as f:
            links = [line.strip() for line in f.readlines()]
            
        for link in links:
            try:
                print(f"Procesando URL: {link}")
                title, text = get_text(link)
                save_texts(title, text, link)
            except Exception as e:
                print(f"Error al grabar texto: {e}")
        
        spain_files, global_files = counter(texts_path)
        print(f"Número de textos escritos en texts/spain: {spain_files}")
        print(f"Número de textos escritos en texts/global: {global_files}")
        print(f"Número total de textos escritos: {spain_files + global_files}")
        
    except Exception as e:
        print(f"Error al leer el archivo de enlaces: {e}")
