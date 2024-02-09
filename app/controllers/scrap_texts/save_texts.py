import os
from controllers.scrap_texts.clean_text import clean_text
from controllers.scrap_texts.clean_filename import clean_filename
from controllers.scrap_texts.remove_header_sspain import remove_header_sspain
from controllers.scrap_texts.remove_multiple_footer import remove_multiple_footer
from controllers.scrap_texts.remove_single_header import remove_single_header
from controllers.scrap_texts.remove_single_footer import remove_single_footer
from dotenv import load_dotenv

load_dotenv()
header = os.getenv("HEADER")
footer = os.getenv("FOOTER")
h_experts = os.getenv("H_EXPERTS")
f_experts = os.getenv("F_EXPERTS")
footer = os.getenv("FOOTER")
subfooter = os.getenv("SUBFOOTER")
spfooter = os.getenv("SPFOOTER")


def save_texts(title, text, url):
    """Save the title and text content to a file, with additional processing steps.
    Args:
        title (str): The title of the text.
        text (str): The content of the text.
        url (str): The URL associated with the text.
    Returns:
        None
    """
    is_url_filtered = True

    current_dir = os.path.dirname(__file__)
    texts_path = os.path.join(current_dir, "../..", "texts")
    spain_path = os.path.join(texts_path, "spain")
    global_path = os.path.join(texts_path, "global")

    clean_url = clean_filename(url)

    if not os.path.exists(texts_path):
        os.makedirs(texts_path)
        os.makedirs(spain_path)
        os.makedirs(global_path)

    file_path = os.path.join(
        spain_path if "scalian-spain" in url else global_path, f"{clean_url}.txt"
    )

    try:
        if "scalian-spain" in url or "scalian.com/es" in url:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)
            clean_text(file_path)

            if "scalian.com/es/experts" in url:
                remove_single_header(file_path, h_experts)
                remove_single_footer(file_path, f_experts)
            elif "scalian-spain" in url:
                remove_single_header(file_path, header)
                remove_multiple_footer(file_path, footer, subfooter)
            elif "scalian.com/es" in url:
                remove_header_sspain(file_path, header)
                remove_single_footer(file_path, spfooter)

            with open(file_path, "r+", encoding="utf-8") as f:
                content = f.read()
                f.seek(0)
                f.write(f"title: {title}\n")
                f.write(f"url: {url}\n\n")
                f.write(content)
            print(f"Texto escrito en texts/{clean_url}.txt\n")
    except Exception as e:
        print(f"Error al escribir texto: {e}")
