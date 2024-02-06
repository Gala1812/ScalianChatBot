from urllib.parse import urlparse


def clean_filename(url):
    parsed_url = urlparse(url)
    host_name = parsed_url.netloc.replace(".", "_")
    path_segments = parsed_url.path.strip("/").split("/")
    path_name = "_".join(path_segments)

    return f"{host_name}_{path_name}"
