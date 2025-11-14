import random
import time
from selenium import By
from bs4 import BeautifulSoup as soup

def obter_altura_atual(driver):
    altura_atual = driver.execute_script("return document.body.scrollHeight")
    return altura_atual

def valor_scroll_aleatorio(min = 600, max = 800):
    return random.randint(min, max)

def pausa_aleatoria(min = 0.3, max = 3):
    return random.uniform(min, max)

def chance_realizar_mini_scroll():
    probabilidade = 7
    valor = random.randrange(100)
    if probabilidade > valor:
        return True
    else:
        return False

def mini_scroll_para_cima(driver):
    valor = random.randint(100, 200)
    driver.execute_script("window.scrollBy(0, arguments[0]);", -valor)

def simular_scroll_humano(driver):
    valor = valor_scroll_aleatorio()
    driver.execute_script("window.scrollBy(0, arguments[0]);", valor)
    time.sleep(pausa_aleatoria())
    if chance_realizar_mini_scroll():
        mini_scroll_para_cima(driver)
        time.sleep(pausa_aleatoria())

def scroll_automatico(driver):
    limite_ciclo = 50
    ciclo = 0
    while ciclo < limite_ciclo:
        altura_inicial = obter_altura_atual(driver)
        simular_scroll_humano(driver)
        altura_nova = obter_altura_atual(driver)
        if altura_nova == altura_inicial:
            break
        ciclo += 1

def coletar_posts_da_pagina(driver):
    return driver.find_elements(By.CSS_SELECTOR, "div[data-urn]")

def extrair_html_do_post(post):
    return post.get_attribute("outerHTML")

def transformar_em_soup(html):
    return soup(html, "html.parser")