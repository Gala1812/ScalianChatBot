import requests
from bs4 import BeautifulSoup
from controllers.check_response_code import check_response_code

def extract_links(url):
    res = requests.get(url)
    res.raise_for_status() 
    try:
        if response := check_response_code(url):
            soup = BeautifulSoup(res.text, "lxml")
            print(f"Extrayendo enlaces de {url}")
            return [link['href'] for link in soup.find_all('a', href=True)]
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener enlaces de {url}: {e}")