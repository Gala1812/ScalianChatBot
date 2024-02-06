from controllers.scrap_links.save_failed_links import save_failed_links
import os
from dotenv import load_dotenv

import requests

load_dotenv()
headers = {'User-Agent': os.getenv("USER_AGENT")}

def check_link_health(url):
    """ Check the health of a given URL.
    Args:
        url (str): The URL to check.
    Returns:
        bool: True if the URL is healthy (returns a status code of 200), False otherwise.
    Raises:
        requests.exceptions.RequestException: If there is an error making the request.
    Examples:
        >>> check_link_health("https://www.example.com")
        True
        >>> check_link_health("https://www.example.com/nonexistent")
        False
    """
    
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        return res.status_code == 200
    except requests.exceptions.RequestException as e:
        save_failed_links([url], "failed_links.txt")
        return False