import pandas as pd
import pickle
from src.nlp.model_utils import *
from sentence_transformers import SentenceTransformer

def predict(df, modelo):
    df = df.reset_index(drop=True)
    texts = prepare_text_column(df, col="texto")
    hashtags = prepare_text_column(df, col="hashtags")
    emb_text = embed_text(texts, modelo_embeddings)
    emb_hash = embed_text(hashtags, modelo_embeddings)
    X = combine_embeddings(emb_text, emb_hash)
    return modelo.predict(X)

df = pd.read_csv("data/raw/posts_linkedin.csv")

modelo_label = pickle.load(open("./models/model_labels.pkl", "rb"))
modelo_senioridade = pickle.load(open("./models/model_sen.pkl", "rb"))
modelo_embeddings = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

df["label"] = predict(df, modelo_label)

mask_vagas = df["label"] == "vaga"
df.loc[mask_vagas, "senioridade"] = predict(df[mask_vagas], modelo_senioridade)
print(df.loc[mask_vagas, "senioridade"].value_counts())

df.to_csv("data/processed/posts_preditos.csv", index=False)
print("Predições concluídas e arquivo salvo!")