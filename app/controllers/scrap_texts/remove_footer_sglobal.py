import os
from dotenv import load_dotenv

load_dotenv()
substring = os.getenv("SUBSTRING2")


def remove_footer_sglobal(text):
    """Remove the footer section from a given text file.
    Args:
        text (str): The path to the text file to remove the footer from.
    Returns:
        None
    """

    with open(text, "r+") as archivo:
        lines = archivo.readlines()
        index_substring = None
        for i in reversed(range(len(lines))):
            if substring.upper() in lines[i].strip().upper():
                index_substring = i
                break

        if index_substring is not None:
            lines = lines[:index_substring]

        archivo.seek(0)
        archivo.truncate()
        archivo.write("".join(lines))
