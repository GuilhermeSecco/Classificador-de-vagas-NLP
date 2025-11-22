"""
Responsável pelo treinamento dos modelos.
"""

from src.nlp.model_utils import *
from src.scraping.scraping_utils.text_cleaning import extrair_senioridade
from sklearn.preprocessing import OneHotEncoder
from sentence_transformers import SentenceTransformer
from scipy.sparse import hstack
import pickle as pkl

#Função principal de treinamento dos modelos
def model_train(y, autor, texts, hashtags, extra_features=None):
    emb_autor = embed_text(autor, model)
    emb_text = embed_text(texts, model)
    emb_hash = embed_text(hashtags, model)
    X = combine_embeddings(emb_autor ,emb_text, emb_hash)
    if extra_features is not None:
        X = hstack([X, extra_features])
    return train_classifier(X, y), X

#Importação do dataset
df = import_dataset("posts_treino.xlsx")
print(df.columns)

#Fazendo a cópia do dataset para o modelo de labels
df_labels = df.copy()

#Preparando as features do modelo
autor = prepare_text_column(df_labels, col="autor")
texts = prepare_text_column(df_labels, col="texto")
hashtags = prepare_text_column(df_labels, col="hashtags")

#Preparando o valor alvo do modelo
labels = prepare_labels(df_labels, col="label")

#Carregando o modelo de NLP
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

#Realizando o treinamento do modelo
model_labels, X_labels = model_train(labels, autor, texts, hashtags)

#Realizando a predição das labels pelo modelo treinado
df_labels["label"] = model_labels.predict(X_labels)

#Fazendo a cópia do dataset para o modelo de senioridade
df_vagas = df[df["label"] == "vaga"].copy().reset_index(drop=True)

#Preparando as colunas de autor, texto e hashtags para o modelo de senioridade
autor_v = prepare_text_column(df_vagas, col="autor")
texts_v = prepare_text_column(df_vagas, col="texto")
hashtags_v = prepare_text_column(df_vagas, col="hashtags")

#Criação do Regex para senioridade
df_vagas["regex_sen"] = df_vagas["texto"].apply(extrair_senioridade)
enc = OneHotEncoder(handle_unknown="ignore")
regex_onehot = enc.fit_transform(df_vagas[["regex_sen"]])

#Salvando o Regex para utilizar nas predições
pkl.dump(enc, open("./models/encoder_regex.pkl", "wb"))

#Valor Alvo do modelo de Senioridade
labels_sen = prepare_seniority_labels(df_vagas, col="senioridade")

#Treinamento do modelo de Senioridade
model_sen, X_sen = model_train(labels_sen, autor_v, texts_v, hashtags_v, extra_features=regex_onehot)

#Realizando Predições com o modelo de senioridade
df.loc[df["label"] == "vaga", "senioridade"] = model_sen.predict(X_sen)

#Salvando os datasets preditos durante o treinamento
df_labels.to_csv("./data/processed/treino_label.csv")
df.to_csv("./data/processed/treino_senioridade.csv", index=False)
print("Predições salvas!\n")

#Salvando os modelos para predições futuras
model_labels_file = "model_labels"
model_sen_file = "model_sen"
model_save(model_labels, model_labels_file)
model_save(model_sen, model_sen_file)