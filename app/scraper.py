from controllers.start_scraping import start_scraping
from controllers.start_downloading_text import start_downloading_text

def main():
    # start_scraping()
    start_downloading_text("links_home_cleaned.txt")

if __name__ == "__main__":
    main()