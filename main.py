from src.driver.driver_setup import iniciar_navegador
from src.driver.cookies import carregar_cookies
from src.scraping.filters import filtrar_busca
from src.scraping.post_scraper import scroll_automatico
import time

if __name__ == "__main__":
    #Iniciando o navegador
    driver = iniciar_navegador()
    driver.maximize_window()

    #Carregando os cookies
    carregar_cookies(driver)

    #Buscando as vagas (Texto = Pesquisa, o periodo pode receber os valores: day = dia, week = semana, month = mês)
    url = filtrar_busca("Machine Learning Brasil", periodo="month")
    driver.get(url)
    time.sleep(4)
    scroll_automatico(driver)
    time.sleep(5)