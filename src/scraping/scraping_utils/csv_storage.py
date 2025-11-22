"""
Salva em Csv após remover posts duplicados
"""

import pandas as pd
import os
from src.scraping.scraping_utils.filtrar_posts_duplicados import remover_posts_duplicados, remover_posts_duplicados_por_similaridade

def salvar_em_csv(posts, caminho):
    novo_df = pd.DataFrame(posts)

    if os.path.exists(caminho):
        antigo_df = pd.read_csv(caminho)

        df = pd.concat([antigo_df, novo_df]).drop_duplicates(subset=["link"], keep="first")
        df = remover_posts_duplicados(df)
        df = remover_posts_duplicados_por_similaridade(df)
        antes = len(antigo_df)
        depois = len(df)
        print(f"{depois - antes} posts novos adicionados.")
    else:
        df = remover_posts_duplicados(novo_df)
        df = remover_posts_duplicados_por_similaridade(df)

    df.to_csv(caminho, index=False)
    print(f"CSV salvo com sucesso ({len(df)} posts no arquivo).")