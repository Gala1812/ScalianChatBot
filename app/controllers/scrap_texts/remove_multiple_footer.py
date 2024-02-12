def remove_multiple_footer(text, footer, substring):
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
                if lines[i].strip().replace(" ", "") == footer
            ),
            None,
        )
        index_substring = next(
            (
                i
                for i in reversed(range(len(lines)))
                if lines[i].strip().replace(" ", "") == substring
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
