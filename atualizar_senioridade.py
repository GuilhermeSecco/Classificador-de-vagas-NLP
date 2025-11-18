import pandas as pd
from src.scraping.scraping_utils.text_cleaning import extrair_senioridade# ou o caminho correto

df = pd.read_excel("./data/processed/posts_com_labels_antigo.xlsx")

# Aplica a função atualizada
df["senioridade"] = df["texto"].astype(str).apply(extrair_senioridade)

# Salva o novo arquivo
df.to_excel("./data/processed/posts_com_labels.xlsx", index=False)

print("✔️ Senioridade atualizada e salva em posts_com_labels.xlsx")