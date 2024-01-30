from controllers.extract_links import extract_links
from controllers.get_all_links import get_all_links
from controllers.get_all_links_more_deep import get_all_links_more_deep
from controllers.merge_links import merge_links
from controllers.write_links import write_links
from controllers.clean_links import clean_links

import os
import time
from dotenv import load_dotenv

load_dotenv()
main_url = os.getenv("URL")

def start_scraping():
    inicio = time.time()
    
    links = extract_links(main_url)
    write_links(links, "links_home.txt")
    cleaned_links = clean_links(links)
    write_links(cleaned_links, "links_home_cleaned.txt")
    
    etapa_1 = time.time() - inicio
    print(f"Tiempo de ejecución de la etapa 1: {etapa_1:.2f} segundos")
    
    first_deep_links = get_all_links(cleaned_links)
    write_links(first_deep_links, "first_deep_links.txt")
    
    etapa_2 = time.time() - inicio
    print(f"Tiempo de ejecución de la etapa 2: {etapa_2:.2f} segundos")
    
    second_deep_links = get_all_links_more_deep(first_deep_links, cleaned_links)
    write_links(second_deep_links, "second_deep_links.txt")
    
    etapa_3 = time.time() - inicio
    minutos = etapa_3 // 60
    segundos = etapa_3 % 60
    
    print(f"Tiempo de ejecución de la etapa 3: {minutos} minutos y {segundos:.2f} segundos")
    
    third_deep_links = get_all_links_more_deep(second_deep_links, first_deep_links)
    write_links(third_deep_links, "third_deep_links.txt")
    
    etapa_4 = time.time() - inicio
    minutos = etapa_4 // 60
    segundos = etapa_4 % 60
    print(f"Tiempo de ejecución de la etapa 4: {minutos} minutos y {segundos:.2f} segundos")
    
    print(f"Cantidad de links: {len(third_deep_links)}")
    
    all_files = ["links_home_cleaned.txt", "first_deep_links.txt", "second_deep_links.txt", "third_deep_links.txt"]
    merge_links(*all_files)