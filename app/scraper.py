from controllers.scrap_texts.download_texts import download_texts
from controllers.start_scraping import start_scraping
import os
from dotenv import load_dotenv

load_dotenv()
filename = os.getenv("FILENAME")

def main():
    # start_scraping()
    download_texts(filename)

if __name__ == "__main__":
    main()