def filtrar_busca(texto, periodo):
    url_base = "https://www.linkedin.com/search/results/content/?"
    texto = texto.replace(" ", "%20")
    url_texto = "&keywords="+ texto
    if periodo == "day":
        periodo = "past-24h"
    elif periodo == "week":
        periodo = "past-week"
    elif periodo == "month":
        periodo = "past-month"
    else:
        periodo = ""
    url_periodo = "datePosted=%22" + periodo + "%22"
    url = url_base + url_periodo + url_texto
    return url