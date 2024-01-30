from controllers.check_response_code import check_response_code
from controllers.extract_links import extract_links
from controllers.clean_links import clean_links

def get_all_links_more_deep(cleaned_links, previous_links):
    all_links = []
    for link in cleaned_links:
        try:
            if response := check_response_code(link):
                if link not in previous_links:
                    extracted_links = extract_links(link)
                    all_links.extend(clean_links(extracted_links))
        except requests.exceptions.RequestException as e:
            print(f"Error al procesar {link}: {e}")
    all_links = list(dict.fromkeys(all_links))
    return clean_links(all_links)