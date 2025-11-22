"""
Limpa, Converte e Separa informações importantes
"""


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
            r"\bvagas\b", r"\boportunidades\b", r"\bv[áa]rias\b"
        ],
        "estagio": [
            r"\best[áa]gio\b", r"\bestagi[áa]rio\b", r"\bintern\b", r"\binternship\b", r"\bestagi[áa]ria\b"
        ],
        "junior": [
            r"\bj[uú]nior\b", r"\bjunior\b", r"\bjr\b", r"\bjuninho\b", r"\bjuniores\b"
        ],
        "pleno": [
            r"\bpleno\b", r"\bmid\b", r"\bmid-level\b", r"\bmid level\b", r"\bespecialista\b", r"\bstaff\b", r"\bexpert\b", r"\specialist\b"
        ],
        "senior": [
            r"\bs[êe]nior\b", r"\bsenior\b", r"\bsr\b", r"\blead\b", r"\btech lead\b", r"\bprincipal\b", r"\bcoordenador\b", r"\bhead\b", r"\blíder\b"
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

def converter_data(data):
    """
    Converte datas nos mais variados formatos para o formato ISO(YYYY-MM-DD)
    """
    #Import das bibliotecas
    import re
    from datetime import date, datetime, timedelta
    import math

    #Carregando a hora atual
    data_atual = datetime.now().date()

    #Carregando o texto
    s = data

    #Garantindo que a data esteja como string e lower
    if isinstance(s, str):
        s = s.strip().lower()

    #Tratamento de valores Nulos
    if s is None:
        return None
    if isinstance(s, float) and math.isnan(s):
        return None
    if isinstance(s, str) and s.strip() == "":
        return None
    if isinstance(s, str) and s.lower() in {"nan", "none"}:
        return None

    #Caso a data esteja em formato ISO, cai nesse funíl
    if isinstance(s, str) and "-" in s:
        try:
            dt = datetime.fromisoformat(s)

            # dt pode ser date OU datetime
            if isinstance(dt, datetime):
                dt = dt.date()  # remove hora

            return dt.strftime("%Y-%m-%d")
        except:
            pass

    #Caso a data esteja no formato brasileiro, passa por esse funíl
    if isinstance(s, str) and "/" in s:
        try:
            dt = datetime.strptime(s, "%d/%m/%Y")
            return dt.date().strftime("%Y-%m-%d")
        except:
            pass

    #Se for datetime remove a hora e formata ao formato correto
    if isinstance(s, datetime):
        return s.date().strftime("%Y-%m-%d")

    #Se já for date, formata para o formato correto
    if isinstance(s, date):
        return s.strftime("%Y-%m-%d")

    #Agora
    if "agora" in s:
        return data_atual.strftime("%Y-%m-%d")

    #Minutos
    if "min" in s:
        n = int(re.findall(r"\d+", s)[0])
        dt = data_atual - timedelta(minutes=n)
        return dt.strftime("%Y-%m-%d")

    #Horas
    if "h" in s and "min" not in s:
        n = int(re.findall(r"\d+", s)[0])
        dt = data_atual - timedelta(hours=n)
        return dt.strftime("%Y-%m-%d")

    #Dias
    if "d" in s:
        n = int(re.findall(r"\d+", s)[0])
        dt = data_atual - timedelta(days=n)
        return dt.strftime("%Y-%m-%d")

    #Semanas
    if "sem" in s:
        n = int(re.findall(r"\d+", s)[0])
        dt = data_atual - timedelta(weeks=n)
        return dt.strftime("%Y-%m-%d")

    #Meses
    if "m" in s and "min" not in s:
        n = int(re.findall(r"\d+", s)[0])
        dt = data_atual - timedelta(days=30 * n)
        return dt.strftime("%Y-%m-%d")

    #Anos
    if "a" in s:
        n = int(re.findall(r"\d+", s)[0])
        dt = data_atual - timedelta(days=365 * n)
        return dt.strftime("%Y-%m-%d")