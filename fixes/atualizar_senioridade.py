#Import das bibliotecas
import pandas as pd
from src.scraping.scraping_utils.text_cleaning import extrair_senioridade

#Carregamento do dataset
df = pd.read_excel("./data/processed/posts_com_labels_antigo.xlsx")

#Aplicação da função extrair_senioridade
df["senioridade"] = df["texto"].astype(str).apply(extrair_senioridade)

#Salvamento do novo .xlsx
df.to_excel("./data/processed/posts_com_labels.xlsx", index=False)

#Print no console
print("Senioridade atualizada e salva em posts_com_labels.xlsx")