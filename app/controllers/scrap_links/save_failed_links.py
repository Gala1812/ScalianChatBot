import os

def save_failed_links(failed_links, file_name):
    current_dir = os.path.dirname(__file__)
    links_path = os.path.join(current_dir, "../..", "links")
    file_path = os.path.join(links_path, file_name)
    
    if not os.path.exists(links_path):
            os.makedirs(links_path)
    try:
        with open(file_path, 'a') as f:
            for link in failed_links:
                f.write(link + '\n')
            print(f"Enlaces fallidos escritos en links/{file_name}")
    except Exception as e:
        print(f"Error al escribir enlaces fallidos: {e}")