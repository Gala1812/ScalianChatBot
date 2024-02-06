from controllers.scrap_links.check_link_health import check_link_health
from controllers.scrap_links.find_links_from_url import find_links_from_url
from controllers.scrap_links.clean_links import clean_links

def get_links_comparing_files(cleaned_links, previous_links):
    """ Get links by comparing cleaned links with previous links.
    Args:
        cleaned_links (list): A list of cleaned links.
        previous_links (list): A list of previously obtained links.
    Returns:
        list: A list of links obtained by comparing the cleaned links with the previous links.
    Raises:
        requests.exceptions.RequestException: If there is an error making a request.
    Examples:
        >>> previous_links = ['https://www.example.com/link2']
        >>> cleaned_links = ['https://www.example.com/link1', 'https://www.example.com/link2']
        >>> get_links_comparing_files(cleaned_links, previous_links)
        ['https://www.example.com/link1']
    """
    
    all_links = []
    for link in cleaned_links:
        try:
            if response := check_link_health(link):
                if link not in previous_links:
                    extracted_links = find_links_from_url(link)
                    all_links.extend(clean_links(extracted_links))
        except requests.exceptions.RequestException as e:
            print(f"Error al procesar {link}: {e}")
    all_links = list(dict.fromkeys(all_links))
    return clean_links(all_links)