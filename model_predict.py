"""
Responsável pelas predições feitas pelos modelos.
"""

import pandas as pd
import pickle
from src.nlp.model_utils import *
from src.scraping.scraping_utils.text_cleaning import extrair_senioridade
from sentence_transformers import SentenceTransformer
from scipy.sparse import hstack

#Função principal de predição dos modelos
def predict(df, modelo, enc=None):
    df = df.reset_index(drop=True)
    autor = prepare_text_column(df, col="autor")
    texts = prepare_text_column(df, col="texto")
    hashtags = prepare_text_column(df, col="hashtags")
    emb_autor = embed_text(autor, modelo_embeddings)
    emb_text = embed_text(texts, modelo_embeddings)
    emb_hash = embed_text(hashtags, modelo_embeddings)
    X = combine_embeddings(emb_autor, emb_text, emb_hash)
    if enc is not None:
        df["regex_sen"] = df["texto"].apply(extrair_senioridade)
        extra = enc.transform(df[["regex_sen"]])
        X = hstack([X, extra])
    return modelo.predict(X)

#Importando Dataset
df = pd.read_csv("data/raw/posts_linkedin.csv")

#Importando Modelos
modelo_label = pickle.load(open("./models/model_labels.pkl", "rb"))
modelo_senioridade = pickle.load(open("./models/model_sen.pkl", "rb"))
modelo_embeddings = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

#Importando Regex
enc = pickle.load(open("./models/encoder_regex.pkl", "rb"))

#Realizando Predição das Labels
df["label"] = predict(df, modelo_label)

#Realizando Predição da Senioridade das vagas
mask_vagas = df["label"] == "vaga"
df.loc[mask_vagas, "senioridade"] = predict(df[mask_vagas], modelo_senioridade, enc=enc)
print(df.loc[mask_vagas, "senioridade"].value_counts())

#Salvando o Csv Resultante
df.to_csv("data/processed/posts_preditos.csv", index=False)
print("Predições concluídas e arquivo salvo!")