import re
import unicodedata

def limpar_repeticao(nome):
    metade = len(nome) // 2
    if nome[:metade] == nome[metade:]:
        return nome[:metade]
    return nome

def limpar_data(data):
    data = data.split("•")[0]
    return data.strip()

def normalizar_unicode(texto):
    return unicodedata.normalize("NFC", texto)

def separar_texto_hashtags(texto):
    palavras = texto.split("hashtag#")
    texto = palavras[0]
    hashtags = []
    if len(palavras) > 1:
        for hashtag in palavras[1:]:
            tag = hashtag.lower().strip().split()[0]
            # Manter só hashtags alfanuméricas
            if re.match(r"^[a-z0-9_]+$", tag):
                hashtags.append(tag)
    return texto, hashtags

def extrair_senioridade(texto):
    texto = texto.lower()

    padroes = {
        "multi": [
            r"\bvagas\b", r"\boportunidades\b"
        ],
        "estagio": [
            r"\best[áa]gio\b", r"\bestagi[áa]rio\b", r"\bintern\b", r"\binternship\b", r"\bestagi[áa]ria\b"
        ],
        "junior": [
            r"\bj[uú]nior\b", r"\bjunior\b", r"\bjr\b", r"\bjuninho\b", r"\bjuniores\b",
        ],
        "pleno": [
            r"\bpleno\b", r"\bmid\b", r"\bmid-level\b", r"\bmid level\b"
        ],
        "senior": [
            r"\bs[êe]nior\b", r"\bsenior\b", r"\bsr\b"
        ],
        "especialista": [
            r"\bespecialista\b", r"\bstaff\b", r"\bexpert\b", r"\specialist\b"
        ],
        "lead": [
            r"\blead\b", r"\btech lead\b", r"\bprincipal\b", r"\bcoordenador\b", r"\bhead\b", r"\blíder\b"
        ],
        "multi": [
            r"junior.*pleno", r"pleno.*senior", r"junior.*senior",
            r"jr.*sr", r"junior e pleno", r"pleno e senior", r"jr e sr"
        ],
    }

    for nivel, regex_list in padroes.items():
        for regex in regex_list:
            if re.search(regex, texto):
                return nivel

    return "não identificado"

def extrair_localizacao(texto):
    texto = texto.lower()
    if "remoto" in texto or "home office" in texto or "remote" in texto:
        return "remoto"
    cidades = ["são paulo", "sp", "rio de janeiro", "rj", "porto alegre", "paraná", "curitiba", "bauru"]
    for cidade in cidades:
        if cidade in texto:
            return cidade
    return "não identificado"

def converter_data(data_str, data_base=None):
    """
    Converte datas relativas do LinkedIn para datas absolutas.
    data_str: string como '1 sem', '3 meses', 'há 4 dias', '25 min'
    data_base: data de coleta (datetime). Se None, usa agora.
    """
    #Import das bibliotecas
    import re
    from datetime import datetime, timedelta

    #Carregando a hora atual
    if data_base is None:
        data_base = datetime.now()

    s = data_str.lower().strip()

    # ---- Agora ----
    if "agora" in s:
        return data_base

    # ---- Minutos ----
    if "min" in s:
        n = int(re.findall(r"\d+", s)[0])
        provavel_data = data_base - timedelta(minutes=n)
        return provavel_data.strftime("%d/%m/%Y")

    # ---- Horas ----
    if "h" in s:
        n = int(re.findall(r"\d+", s)[0])
        provavel_data = data_base - timedelta(hours=n)
        return provavel_data.strftime("%d/%m/%Y")

    # ---- Dias ----
    if "d" in s:
        n = int(re.findall(r"\d+", s)[0])
        provavel_data = data_base - timedelta(days=n)
        return provavel_data.strftime("%d/%m/%Y")

    # ---- Semanas ----
    if "sem" in s:
        n = int(re.findall(r"\d+", s)[0])
        provavel_data = data_base - timedelta(weeks=n)
        return provavel_data.strftime("%d/%m/%Y")

    # ---- Meses ----
    # Usamos 30 dias como aproximação
    if "m" in s:
        n = int(re.findall(r"\d+", s)[0])
        provavel_data = data_base - timedelta(days=30 * n)
        return provavel_data.strftime("%d/%m/%Y")

    # ---- Anos ----
    if "a" in s:
        n = int(re.findall(r"\d+", s)[0])
        provavel_data = data_base - timedelta(days=365 * n)
        return provavel_data.strftime("%d/%m/%Y")

    try:
        return datetime.strptime(s, "%d/%m/%Y")
    except:
        return None