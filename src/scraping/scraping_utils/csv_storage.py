import pandas as pd
import os

def salvar_em_csv(posts, caminho):
    novo_df = pd.DataFrame(posts)

    if os.path.exists(caminho):
        antigo_df = pd.read_csv(caminho)

        df = pd.concat([antigo_df, novo_df]).drop_duplicates(subset=["link"], keep="first")
        antes = len(antigo_df)
        depois = len(df)
        print(f"{depois - antes} posts novos adicionados.")
    else:
        df = novo_df

    df.to_csv(caminho, index=False)
    print(f"CSV salvo com sucesso ({len(df)} posts no arquivo).")