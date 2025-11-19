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
    #Prepara a coluna "texto"
    return df[col].astype(str).fillna("")

def prepare_labels(df, col='Label'):
    #Prepara a coluna "label"
    return df[col].astype(str)

def prepare_seniority_labels(df, col="senioridade"):
    #Prepara a coluna "senioridade"
    return df[col].astype(str)

def embed_text(texts, model=None):
    #Import do NLP
    from sentence_transformers import SentenceTransformer

    #Carregamento do modelo
    if model is None:
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    #Retorno do texto após a aplicação do modelo
    return model.encode(texts, show_progress_bar=True)

def combine_embeddings(*arrays):
    #Importação do Numpy
    import numpy as np
    # Combina as colunas que serão utilizadas na classificação
    return np.hstack(arrays)

def train_classifier(X, y):
    #Import das bibliotecas
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report

    #Separação do dataset entre treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #Carregamento do modelo de regressão logística
    clf = LogisticRegression(max_iter=2000)

    #Treinamento do Modelo
    clf.fit(X_train, y_train)

    #Teste do Modelo
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))

    #Retornando o modelo treinado e testado
    return clf

def model_save(model, nome_modelo):
    #Import do pickle
    import pickle

    #Especificando diretório e nome do modelo
    path = "models/" + nome_modelo + ".pkl"

    try:
        #Tenta salvar o modelo
        with open(path, 'wb') as file:
            pickle.dump(model, file)
        print(f"Modelo salvo em: {path}")
    #Em casos de erro, o erro é descrito no console
    except Exception as e:
        print(f"Error saving object: {e}")