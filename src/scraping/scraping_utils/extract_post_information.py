"""
Extrai informações do post utilizando Selenium e BeautifulSoup
"""

from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as soup
from src.scraping.scraping_utils.text_cleaning import limpar_repeticao, limpar_data, converter_data

def coletar_posts_da_pagina(driver):
    return driver.find_elements(By.CSS_SELECTOR, "div[data-urn]")

def extrair_html_do_post(post):
    return post.get_attribute("outerHTML")

def transformar_em_soup(html):
    return soup(html, "html.parser")

def extrair_autor_post(soup):
    autor = soup.select_one("span.update-components-actor__single-line-truncate")
    if autor:
        nome = autor.get_text(strip=True)
        nome = limpar_repeticao(nome)
        return nome
    else:
        return ""

def extrair_texto_post(soup):
    post = soup.find("span", class_="break-words")
    if post:
        texto = post.get_text(strip=True)
        return texto
    else:
        return ""

def extrair_data_post(soup):
    bloco = soup.select_one("span.update-components-actor__sub-description")
    if bloco:
        data_span = bloco.find("span")
        if data_span:
            texto = data_span.get_text(strip=True)
            texto = limpar_data(texto)
            data_abs = converter_data(texto)
            if data_abs:
                return data_abs

def extrair_link_post(soup):
    # Procurar links prováveis a partir de padrões do LinkedIn
    link = soup.find("a", href=lambda href: href and (
        "/feed/update" in href or
        "/posts/" in href or
        "linkedin.com/posts" in href or
        "activity" in href or
        "share" in href
    ))
    if link:
        href = link.get("href")
        if href.startswith("/"):
            href = "https://www.linkedin.com" + href
        return href.split("?")[0]  # Remove parâmetros desnecessários
    return ""

def gerar_link_do_post(post_selenium):
    urn = post_selenium.get_attribute("data-urn")
    if urn and "activity" in urn:
        return f"https://www.linkedin.com/feed/update/{urn}"
    return ""