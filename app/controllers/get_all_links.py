from controllers.check_response_code import check_response_code
from controllers.extract_links import extract_links
from controllers.clean_links import clean_links

def get_all_links(cleaned_links):
    all_links = []
    for link in cleaned_links:
        if status_code := check_response_code(link):
            try:
                extracted_links = extract_links(link)
                all_links.extend(clean_links(extracted_links))
            except Exception as e:
                print(f"Error al procesar {link}: {e}")
    all_links = list(dict.fromkeys(all_links))
    return clean_links(all_links)