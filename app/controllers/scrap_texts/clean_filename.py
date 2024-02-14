from urllib.parse import urlparse


def clean_filename(url):
    """ Clean a URL and generate a clean filename.
    Args:
        url (str): The URL to clean.
    Returns:
        str: The cleaned filename generated from the URL.
    Examples:
        >>> clean_filename("https://www.example.com/path/to/file.html")
        'www_example_com_path_to_file_html'
    """
    
    parsed_url = urlparse(url)
    host_name = parsed_url.netloc.replace(".", "_")
    path_segments = parsed_url.path.strip("/").split("/")
    path_name = "_".join(path_segments)

    return f"{host_name}_{path_name}"
