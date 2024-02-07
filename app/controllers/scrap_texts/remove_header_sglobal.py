import os
from dotenv import load_dotenv

load_dotenv()
header = os.getenv("HEADER2")


def remove_header_sglobal(texto):
    """Remove the header section from a given text file.
    Args:
        texto (str): The path to the text file to remove the header from.
    Returns:
        None
    """

    with open(texto, "r+") as archivo:
        lines = archivo.readlines()
        index_join_us = next(
            (i + 1 for i in reversed(range(len(lines))) if lines[i].strip() == header),
            None,
        )
        print(f"Encontre el header {header} en la linea {index_join_us}")
        if index_join_us is not None:
            lines = lines[index_join_us:]
            doc = "".join(lines)
            archivo.seek(0)
            archivo.truncate()
            archivo.write(doc)
