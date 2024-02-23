import os

def save_links(links, file_name):
    """ Save a list of links to a file.
    Args:
        links (list): A list of links to save.
        file_name (str): The name of the file to save the links.
    Returns:
        None
    Examples:
        >>> links = ['https://www.example.com/link1', 'https://www.example.com/link2']
        >>> save_links(links, "saved_links.txt")
        Enlaces escritos en links/saved_links.txt
    """
    
    current_dir = os.path.dirname(__file__)
    links_path = os.path.join(current_dir, "../..", "links")
    file_path = os.path.join(links_path, file_name)
    
    if not os.path.exists(links_path):
            os.makedirs(links_path)
    try:
        with open(file_path, 'w') as f:
            for link in links:
                f.write(link + '\n')
        print(f"Enlaces escritos en links/{file_name}")
    except Exception as e:
        print(f"Error al escribir enlaces: {e}")