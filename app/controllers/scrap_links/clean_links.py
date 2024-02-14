from urllib.parse import urlparse, urlunparse


def clean_links(links):
    """ Clean a list of links by removing unwanted links based on specified criteria.
    Args:
        links (list): A list of links to be cleaned.
    Returns:
        list: A list of cleaned links that meet the specified criteria.

    Examples:
        >>> links = [
        ...     "https://www.example.com",
        ...     "https://www.linkedin.com",
        ...     "https://www.example.com/file.pdf"
        ... ]
        >>> clean_links(links)
        ['https://www.example.com']
    """
    
    allowed_domains = ["scalian.com", "scalian-spain.es"]

    ignored_host = [
        "linkedin",
        "instagram",
        "twitter",
        "indizen",
        "cookieyes",
        "wordpress",
        "g2",
        "capterra",
        "facebook",
        "youtube",
    ]

    ignored_extensions = [
        "pdf",
        "jpg",
        "jpeg",
        "png",
        "doc",
        "docx",
        "xls",
        "xlsx",
        "ppt",
        "pptx",
        "zip",
        "rar",
        "7z",
        "tar",
        "gz",
        "tgz",
        "mp3",
        "mp4",
        "avi",
        "mov",
        "wmv",
        "flv",
        "wav",
        "aiff",
        "wma",
        "ogg",
        "webm",
        "m4a",
        "aac",
        "flac",
        "alac",
        "wma",
        "bmp",
        "gif",
        "tiff",
        "psd",
        "raw",
        "svg",
        "eps",
        "ai",
    ]

    try:
        links = [
            urlunparse(
                urlparse(link)._replace(
                    netloc=urlparse(link).netloc.replace("www.www.", "www.")
                )
            )
            for link in links
            if all(host not in link.lower() for host in ignored_host)
            and not any(link.lower().endswith(ext) for ext in ignored_extensions)
            and link.startswith("https://")
            and any(domain in urlparse(link).netloc for domain in allowed_domains)
        ]
        links = list(set(links))
        print("Limpiando enlaces ...\n")
    except Exception as e:
        print(f"Error al limpiar enlaces: {e}")

    return links
