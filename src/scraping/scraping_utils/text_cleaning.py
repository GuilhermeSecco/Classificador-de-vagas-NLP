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
    if "estágio" in texto or "estagiário" in texto or "intern" in texto or "estagio" in texto or "estagiario" in texto:
        return "estagio"
    if "júnior" in texto or "junior" in texto or "jr" in texto:
        return "junior"
    if "pleno" in texto or "mid" in texto:
        return "pleno"
    if "sênior" in texto or "senior" in texto or "sr" in texto:
        return "senior"
    if "lead" in texto or "tech lead" in texto or "coordenador" in texto:
        return "lead"
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