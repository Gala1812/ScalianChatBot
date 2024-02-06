def remove_header_sspain(texto):
    """ Remove the header section from a given text file.
    Args:
        texto (str): The path to the text file to remove the header from.
    Returns:
        None
    """
    
    with open(texto, "r+") as archivo:
        lines = archivo.readlines()
        index_join_us = next(
            (
                i + 1
                for i in reversed(range(len(lines)))
                if lines[i].strip().upper() == "JOIN US"
            ),
            None,
        )
        if index_join_us is not None:
            lines = lines[index_join_us:]
            doc = "".join(lines)
            archivo.seek(0)
            archivo.truncate()
            archivo.write(doc)
