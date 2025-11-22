"""
Filtrar e remove posts duplicados
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def remover_posts_duplicados(df):
    """
    Remove duplicações de posts do LinkedIn:
    - mesmo texto + mesma data
    - texto semelhante (normalizado)
    """

    # Normalizar texto
    if "texto" in df.columns:
        df["texto_limpo"] = (
            df["texto"]
            .astype(str)
            .str.lower()
            .str.replace(r"\s+", " ", regex=True)
            .str.replace(r"[^\w\s]", "", regex=True)
            .str.strip()
        )

    #Duplicatas por texto + data
    if "data" in df.columns:
        df = df.drop_duplicates(subset=["texto_limpo", "data"], keep="first")

    #Duplicatas por texto normalizado (caso não tenha data)
    df = df.drop_duplicates(subset=["texto_limpo"], keep="first")

    #Remover coluna auxiliar
    df = df.drop(columns=["texto_limpo"], errors="ignore")

    return df

def remover_posts_duplicados_por_similaridade(df, threshold=0.92):
    """
    Remove posts com texto muito semelhante utilizando TF-IDF + cosine similarity.
    """

    #Normalizar texto
    textos = (
        df["texto"]
        .astype(str)
        .str.lower()
        .str.replace(r"\s+", " ", regex=True)
        .str.replace(r"[^\w\s]", "", regex=True)
        .str.strip()
    )

    #Vetorização
    vectorizer = TfidfVectorizer(min_df=2)
    X = vectorizer.fit_transform(textos)

    #Similaridade de cosseno
    sim = cosine_similarity(X)

    #Identificar duplicados
    to_drop = set()
    n = len(df)

    for i in range(n):
        if i in to_drop:
            continue
        similares = np.where(sim[i] > threshold)[0]
        for j in similares:
            if j != i:
                to_drop.add(j)

    #Remover duplicados
    df_filtrado = df.drop(df.index[list(to_drop)]).reset_index(drop=True)
    print(f"{len(to_drop)} posts removidos por similaridade > {threshold}")

    return df_filtrado