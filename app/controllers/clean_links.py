def clean_links(links):
    ignored_host = ['linkedin', 'instagram', 'twitter', 'indizen', 'cookieyes', 'wordpress', 'g2', 'capterra', 'facebook', 'youtube', 'png', 'jpg']
    try:
        links = [
            link
            for link in links
            if link.startswith('https://')
            and all(host not in link for host in ignored_host)
        ]
        links = list(dict.fromkeys(links))
        print("Limpiando enlaces ...\n")
    except Exception as e:
        print(f"Error al limpiar enlaces: {e}")
    return links