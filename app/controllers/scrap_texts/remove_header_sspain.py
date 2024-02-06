def remove_header_sspain(texto):
    with open(texto, "r+") as archivo:
        lineas = archivo.readlines()
        indice_join_us = None
        for i in reversed(range(len(lineas))):
            if lineas[i].strip().upper() == "JOIN US":
                indice_join_us = i + 1
                break

        if indice_join_us is not None:
            lineas = lineas[indice_join_us:]
            doc = "".join(lineas)
            archivo.seek(0)
            archivo.truncate()
            archivo.write(doc)
