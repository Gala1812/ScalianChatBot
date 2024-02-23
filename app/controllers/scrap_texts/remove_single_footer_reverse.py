def remove_single_footer_reverse(text, footer):
    """Remove the footer section from a given text file.
    Args:
        text (str): The path to the text file to remove the footer from.
    Returns:
        None
    """

    with open(text, "r+") as archivo:
        lines = archivo.readlines()
        index = next(
            (
                i - 1
                for i in range(len(lines))
                if lines[i].strip().replace(" ", "") == footer
            ),
            None,
        )
        if index is not None:
            lines = lines[:index]

        archivo.seek(0)
        archivo.truncate()
        archivo.write("".join(lines))