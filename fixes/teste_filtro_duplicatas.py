import pandas as pd
from src.scraping.scraping_utils.filtrar_posts_duplicados import remover_posts_duplicados, remover_posts_duplicados_por_similaridade

antigo_df = pd.read_csv("../data/raw/posts_linkedin.csv")
antes = len(antigo_df)
print(f"O data set original possuia {antes} posts")

df = remover_posts_duplicados(antigo_df)
depois = len(df)
print(f"{antes - depois} posts foram removidos com o uso do remover_posts_duplicados.")
df = remover_posts_duplicados_por_similaridade(df, threshold=0.92)
depois = len(df)