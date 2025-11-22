#Import das bibliotecas
import pandas as pd
from src.scraping.scraping_utils.text_cleaning import converter_data

#Carregamento do dataset
df = pd.read_excel("../data/raw/posts_com_labels.xlsx")
df_coletado = pd.read_csv("../data/raw/posts_linkedin.csv")

#Print para verificar as datas
print(df["data"].unique())
print(df_coletado["data"].unique())

#Conversão das datas para o novo formato padrão
df["data"] = df["data"].apply(converter_data)
df_coletado["data"] = df_coletado["data"].apply(converter_data)

#Print para verificar se tudo deu certo
print(df["data"].unique())
print(df_coletado["data"].unique())

#Export do novo dataset
df.to_excel("../data/raw/posts_com_labels.xlsx", index=False)
df_coletado.to_csv("../data/raw/posts_linkedin.csv")
print("Datas Atualizadas com Sucesso!")