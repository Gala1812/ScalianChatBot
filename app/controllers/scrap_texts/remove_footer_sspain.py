import os
from dotenv import load_dotenv

load_dotenv()
footer = os.getenv("FOOTER")
substring = os.getenv("SUBSTRING")


def remove_footer_sspain(text):
    """Remove the footer section from a given text file.
    Args:
        text (str): The path to the text file to remove the footer from.
    Returns:
        None
    """

    with open(text, "r+") as archivo:
        lines = archivo.readlines()

        index_footer = next(
            (
                i
                for i in reversed(range(len(lines)))
                if lines[i].strip().upper() == footer
            ),
            None,
        )
        index_substring = next(
            (
                i
                for i in reversed(range(len(lines)))
                if substring.upper() in lines[i].strip().upper()
            ),
            None,
        )
        if index_footer is not None:
            lines = lines[:index_footer]

        if index_substring is not None:
            lines = lines[:index_substring]

        archivo.seek(0)
        archivo.truncate()
        archivo.write("".join(lines))
