import requests
from bs4 import BeautifulSoup
from controllers.scrap_links.check_link_health import check_link_health

def find_links_from_url(url):
    """ Find and extract links from a given URL.
    Args:
        url (str): The URL to extract links from.
    Returns:
        list: A list of links found on the webpage.
    Raises:
        requests.exceptions.RequestException: If there is an error making the request.
    Examples:
        >>> find_links_from_url("https://www.example.com")
        ['https://www.example.com/link1', 'https://www.example.com/link2']
    """
    
    res = requests.get(url)
    res.raise_for_status() 
    try:
        if response := check_link_health(url):
            soup = BeautifulSoup(res.text, "lxml")
            print(f"Extrayendo enlaces de {url}")
            return [link['href'] for link in soup.find_all('a', href=True)]
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener enlaces de {url}: {e}")