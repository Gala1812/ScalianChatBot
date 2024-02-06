import os


def merge_files_with_links(*archivos):
    """ Merge multiple files containing links into a single file.
    Args:
        *archivos (str): Variable number of file names to merge.
    Returns:
        None
    Examples:
        >>> merge_files_with_links("file1.txt", "file2.txt", "file3.txt")
        Se encontraron 100 enlaces
        Enlaces unidos con éxito
    """
    
    enlaces_totales = set()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "..", "..")
    links_path = os.path.join(app_path, "links")
    file_name = "total_links.txt"
    file_path = os.path.join(links_path, file_name)

    if not os.path.exists(links_path):
        os.makedirs(links_path)

    try:
        for archivo in archivos:
            input_file_path = os.path.join(links_path, archivo)

            with open(input_file_path, "r") as f:
                enlaces = f.readlines()
                enlaces_totales.update(enlaces)

        enlaces_totales = list(enlaces_totales)
        print(f"Se encontraron {len(enlaces_totales)} enlaces")

        with open(file_path, "w") as f:
            f.writelines(enlaces_totales)
            print("Enlaces unidos con éxito\n")
    except Exception as e:
        print(f"Error al escribir enlaces: {e}")
