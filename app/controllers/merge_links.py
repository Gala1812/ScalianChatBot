import os

def merge_links(*archivos):
    enlaces_totales = set()
    current_dir = os.path.dirname(__file__)
    links_path = os.path.join(current_dir, "..", "links")
    
    if not os.path.exists(links_path):
            os.makedirs(links_path)
    try:
        for archivo in archivos:
            file_path = os.path.join(links_path, archivo)
            with open(file_path, 'r') as f:
                enlaces = f.readlines()
                enlaces_totales.update(enlaces)
        enlaces_totales = list(enlaces_totales)
        with open('enlaces_totales.txt', 'w') as f:
            f.writelines(enlaces_totales)
    except Exception as e:
        print(f"Error al escribir enlaces: {e}")