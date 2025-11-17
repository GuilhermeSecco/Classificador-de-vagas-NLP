import random
import time
from src.scraping.scraping_utils.waits import pausa_aleatoria

def obter_altura_atual(driver):
    altura_atual = driver.execute_script("return document.body.scrollHeight")
    return altura_atual

def valor_scroll_aleatorio(min = 300, max = 800):
    return random.randint(min, max)

def chance_realizar_mini_scroll(chance = 15):
    probabilidade = chance
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
    driver.execute_script("window.scrollBy({top: arguments[0], behavior: 'smooth'});", valor)
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