"""
Módulo: model_utils.py
Responsável pelo pré-processamento inicial dos dados antes das etapas de transformação e modelagem.

Etapas implementadas:
1. Importação do dataset bruto.
2. Preparação das colunas textuais.
3. Preparação das labels.
4. Embedding do texto.
5. Combinação dos Embeddings.
6. Treino, teste e relatório do modelo de classificação.
"""

def import_dataset(df):
    """
    Importa um arquivo CSV da pasta data/raw/ e retorna um DataFrame.
    Parâmetros:
    : df ⇾ nome do arquivo (sem extensão):
    Retorna:
    : Dataframe com os dados:
    """
    import pandas as pd
    pd.set_option('display.max_columns', None)  # Mostra todas as colunas
    pd.set_option('display.width', None)
    return pd.read_excel(f"./data/processed/{df}.xlsx")

def prepare_text_column(df, col='texto'):
    return df[col].astype(str).fillna("")

def prepare_labels(df, col='Label'):
    return df[col].astype(str)

def prepare_seniority_labels(df, col="senioridade"):
    return df[col].astype(str)

def embed_text(texts, model=None):
    from sentence_transformers import SentenceTransformer

    if model is None:
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    return model.encode(texts, show_progress_bar=True)

def combine_embeddings(*arrays):
    import numpy as np
    return np.hstack(arrays)

def train_classifier(X, y):
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=9)

    clf = LogisticRegression(max_iter=2000)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))

    return clf

def model_save(model, nome_modelo):
    import pickle
    path = "models/" + nome_modelo + ".pkl"
    try:
        with open(path, 'wb') as file:
            pickle.dump(model, file)
        print(f"Modelo salvo em: {path}")
    except Exception as e:
        print(f"Error saving object: {e}")