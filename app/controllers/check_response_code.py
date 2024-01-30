from controllers.write_failed_links import write_failed_links
import os
from dotenv import load_dotenv
import requests

load_dotenv()
headers = {'User-Agent': os.getenv("USER_AGENT")}

def check_response_code(url):
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        return res.status_code == 200
    except requests.exceptions.RequestException as e:
        write_failed_links([url], "failed_links.txt")
        return False