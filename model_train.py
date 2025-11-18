from src.nlp.model_utils import *

def model_train(valor_alvo, texts, hashtags):
    emb_text = embed_text(texts, model)
    emb_hash = embed_text(hashtags, model)
    X = combine_embeddings(emb_text, emb_hash)
    return train_classifier(X, valor_alvo), X

df = import_dataset("posts_com_labels")
print(df.columns)

texts = prepare_text_column(df, col="texto")
hashtags = prepare_text_column(df, col="hashtags")
labels = prepare_labels(df, col="tipo")

from sentence_transformers import SentenceTransformer
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

model_labels, X_labels = model_train(labels, texts, hashtags)

df.rename(columns={"tipo": "label"}, inplace=True)
df["label"] = model_labels.predict(X_labels)

df_vagas = df[df["label"] == "vaga"].copy().reset_index(drop=True)

texts_v = prepare_text_column(df_vagas, col="texto")
hashtags_v = prepare_text_column(df_vagas, col="hashtags")
labels_sen = prepare_seniority_labels(df_vagas, col="senioridade")

model_sen, X_sen = model_train(labels_sen, texts_v, hashtags_v)

df.loc[df["label"] == "vaga", "senioridade"] = model_sen.predict(X_sen)

df.to_csv("./data/processed/posts_com_predicoes_treino.csv", index=False)
print("Predições salvas!\n")

model_labels_file = "model_labels"
model_sen_file = "model_sen"

model_save(model_labels, model_labels_file)
model_save(model_sen, model_sen_file)