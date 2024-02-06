import os

def save_failed_links(failed_links, file_name):
    """ Save a list of failed links to a file.
    Args:
        failed_links (list): A list of failed links.
        file_name (str): The name of the file to save the failed links.
    Returns:
        None
    Examples:
        >>> failed_links = ['https://www.example.com/link1', 'https://www.example.com/link2']
        >>> save_failed_links(failed_links, "failed_links.txt")
        Enlaces fallidos escritos en links/failed_links.txt
    """
    
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