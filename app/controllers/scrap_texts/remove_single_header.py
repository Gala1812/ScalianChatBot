def remove_single_header(texto, header):
    """Remove the header section from a given text file.
    Args:
        texto (str): The path to the text file to remove the header from.
    Returns:
        None
    """

    with open(texto, "r+") as archivo:
        lines = archivo.readlines()
        index = next(
            (
                i + 1
                for i in range(len(lines))
                if lines[i].strip().replace(" ", "") == header
            ),
            None,
        )
        if index is not None:
            lines = lines[index:]
            doc = "".join(lines)
            archivo.seek(0)
            archivo.truncate()
            archivo.write(doc)