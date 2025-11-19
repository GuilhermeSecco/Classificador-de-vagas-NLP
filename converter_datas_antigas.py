import pandas as pd

from src.scraping.scraping_utils.text_cleaning import converter_data

df = pd.read_excel("data/processed/posts_com_labels.xlsx")

print(df["data"].unique())

df["data"] = df["data"].apply(converter_data)

print(df["data"].unique())

df.to_excel("data/processed/posts_com_labels.xlsx", index=False)