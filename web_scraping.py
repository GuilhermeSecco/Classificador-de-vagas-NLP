from src.scraping.scraping_utils.driver_setup import iniciar_navegador
from src.scraping.scraping_utils.cookies import carregar_cookies
from src.scraping.scraping_utils.post_filters import filtrar_busca
from src.scraping.scraping_utils.csv_storage import salvar_em_csv
from src.scraping.post_scraper import coletar_posts_driver
import time

if __name__ == "__main__":
    #Iniciando o navegador
    driver = iniciar_navegador()
    driver.maximize_window()

    #Carregando os cookies
    carregar_cookies(driver)

    #Buscando as vagas (Texto = Pesquisa, o período pode receber os valores: day = dia, week = semana, month = mês)
    url = filtrar_busca("Vaga Python", periodo="week")
    driver.get(url)
    time.sleep(4)

    #Coleta dos Posts
    posts = coletar_posts_driver(driver)

    #Salvando novos posts em .csv
    salvar_em_csv(posts, "./data/raw/posts_linkedin.csv")