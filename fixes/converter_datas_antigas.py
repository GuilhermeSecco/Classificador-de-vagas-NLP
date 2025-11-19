#Import das bibliotecas
import pandas as pd
from src.scraping.scraping_utils.text_cleaning import converter_data

#Carregamento do dataset
df = pd.read_excel("../data/processed/posts_com_labels.xlsx")

#Print para verificar as datas
print(df["data"].unique())

#Conversão das datas para o novo formato
df["data"] = df["data"].apply(converter_data)

#Print para verificar se tudo deu certo
print(df["data"].unique())

#Export do novo dataset
df.to_excel("data/processed/posts_com_labels.xlsx", index=False)