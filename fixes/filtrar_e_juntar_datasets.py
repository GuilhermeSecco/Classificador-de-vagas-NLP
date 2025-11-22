import pandas as pd
from src.scraping.scraping_utils.filtrar_posts_duplicados import *

df = pd.read_csv("../data/raw/posts_linkedin.csv")
df_limpo = remover_posts_duplicados(df)
df_limpo = remover_posts_duplicados_por_similaridade(df_limpo)
df_limpo.to_csv("../data/raw/posts_linkedin.csv", index=False)
df_labels = pd.read_excel("../data/raw/posts_com_labels.xlsx")
df_merge = df_limpo.merge(df_labels, how="left", on="link")
df_merge.to_excel("../data/raw/posts_treino.xlsx", index=False)