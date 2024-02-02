from controllers.scrap_links.check_link_health import check_link_health
from controllers.scrap_links.find_links_from_url import find_links_from_url
from controllers.scrap_links.clean_links import clean_links

def get_links_from_file(cleaned_links):
    all_links = []
    for link in cleaned_links:
        if status_code := check_link_health(link):
            try:
                extracted_links = find_links_from_url(link)
                all_links.extend(clean_links(extracted_links))
            except Exception as e:
                print(f"Error al procesar {link}: {e}")
    all_links = list(dict.fromkeys(all_links))
    return clean_links(all_links)