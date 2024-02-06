def remove_footer_sspain(text):
    """ Remove the footer section from a given text file.
    Args:
        text (str): The path to the text file to remove the footer from.
    Returns:
        None
    """
    
    with open(text, "r+") as archivo:
        lines = archivo.readlines()
        index_join_us = next(
            (
                i - 1
                for i in reversed(range(len(lines)))
                if lines[i].strip().upper() == "ISO 9001"
            ),
            None,
        )
        if index_join_us is not None:
            lines = lines[:index_join_us]
            doc = "".join(lines)
            archivo.seek(0)
            archivo.truncate()
            archivo.write(doc)
