from src.scraping.scraping_utils.scrolling import scroll_automatico
from src.scraping.scraping_utils.extract_post_data import *
from src.scraping.scraping_utils.text_cleaning import *

def coletar_posts_driver(driver, max_posts=300):
    posts_extraidos = []
    tentativas_sem_novos_posts = 0

    while len(posts_extraidos) < max_posts and tentativas_sem_novos_posts < 5:
        scroll_automatico(driver)
        posts_selenium = coletar_posts_da_pagina(driver)

        novos_posts = 0

        for post in posts_selenium:
            if len(posts_extraidos) >= max_posts:
                break

            html = extrair_html_do_post(post)
            soup = transformar_em_soup(html)
            autor = extrair_autor_post(soup)
            texto = extrair_texto_post(soup)
            texto = normalizar_unicode(texto)
            texto, hashtags = separar_texto_hashtags(texto)
            data = extrair_data_post(soup)
            link = gerar_link_do_post(post)
            senioridade = extrair_senioridade(texto)
            localizacao = extrair_localizacao(texto)
            if texto and autor:
                post_data = {
                    "autor": autor,
                    "texto": texto,
                    "data": data,
                    "link": link,
                    "hashtags": hashtags,
                    "senioridade": senioridade,
                    "localizacao": localizacao
                }

                if post_data not in posts_extraidos:
                    posts_extraidos.append(post_data)
                    novos_posts += 1

        if novos_posts == 0:
            tentativas_sem_novos_posts += 1
        else:
            tentativas_sem_novos_posts = 0

    return posts_extraidos