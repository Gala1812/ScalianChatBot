from controllers.scrap_links.find_links_from_url import find_links_from_url
from controllers.scrap_links.get_links_from_file import get_links_from_file
from controllers.scrap_links.get_links_comparing_files import get_links_comparing_files
from controllers.scrap_links.merge_files_with_links import merge_files_with_links
from controllers.scrap_links.save_links import save_links
from controllers.scrap_links.clean_links import clean_links

import os
import time
from dotenv import load_dotenv

load_dotenv()
main_url = os.getenv("URL")


def start_scraping():
    inicio = time.time()

    links = find_links_from_url(main_url)
    save_links(links, "links_home.txt")
    cleaned_links = clean_links(links)
    save_links(cleaned_links, "links_home_cleaned.txt")

    etapa_1 = time.time() - inicio
    print(f"Tiempo de ejecución de la etapa 1: {etapa_1:.2f} segundos")

    first_deep_links = get_links_from_file(cleaned_links)
    save_links(first_deep_links, "first_deep_links.txt")

    etapa_2 = time.time() - inicio
    print(f"Tiempo de ejecución de la etapa 2: {etapa_2:.2f} segundos")

    second_deep_links = get_links_comparing_files(first_deep_links, cleaned_links)
    save_links(second_deep_links, "second_deep_links.txt")

    etapa_3 = time.time() - inicio
    minutos = etapa_3 // 60
    segundos = etapa_3 % 60

    print(
        f"Tiempo de ejecución de la etapa 3: {minutos} minutos y {segundos:.2f} segundos"
    )

    third_deep_links = get_links_comparing_files(second_deep_links, first_deep_links)
    save_links(third_deep_links, "third_deep_links.txt")

    etapa_4 = time.time() - inicio
    minutos = etapa_4 // 60
    segundos = etapa_4 % 60
    print(
        f"Tiempo de ejecución de la etapa 4: {minutos} minutos y {segundos:.2f} segundos"
    )

    print(f"Cantidad de links: {len(third_deep_links)}")

    all_files = [
        "links_home_cleaned.txt",
        "first_deep_links.txt",
        "second_deep_links.txt",
        "third_deep_links.txt",
    ]
    merge_files_with_links(*all_files)
