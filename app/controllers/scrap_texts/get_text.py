import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()
headers = {'User-Agent': os.getenv("USER_AGENT")}

def get_text(url):
    """ Get the title and text content from a given URL.
    Args:
        url (str): The URL to retrieve the text from.
    Returns:
        tuple: A tuple containing the title and text content of the webpage.
    Examples:
        >>> get_text("https://www.example.com")
        ('Example Domain', 'This is an example domain.')
    """
    
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        title = soup.title.text.strip()
        text = soup.get_text().strip()
        return title, text
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener texto de {url}: {e}")
        return ""
    except requests.exceptions.ConnectionError as e:
        print(f"Error de conexión al obtener texto de {url}: {e}")
        return ""