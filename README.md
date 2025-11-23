# Classificador de Vagas
> 

## 🧠 Visão Geral

Este projeto é um pipeline completo de Web Scraping + NLP + Machine Learning, desenvolvido para coletar publicações do LinkedIn, tratá-las, remover duplicatas e classificar automaticamente:

    O tipo do post (vaga, postagem comum ou conteúdo estrangeiro)

    A senioridade da vaga (estágio, júnior, pleno, sênior ou multi-nível)

A solução combina: 

    Extração automatizada com Selenium e BeautifulSoup.
      
    Limpeza e padronização dos dados.
      
    Embeddings com Sentence-BERT.
      
    Modelos de classificação com Regressão Logística
      
    Processo de deduplicação baseado em similaridade textual.
      

O projeto está em fase de preparação para deploy no portfólio, permitindo que qualquer usuário cole o link de uma vaga e receba uma análise automática em tempo real.

## 🧬 Arquitetura do Projeto
    📁 Classificador-de-vagas-NLP/
    │
    ├── .venv/                         # Ambiente virtual
    ├── .python-version
    ├── pyproject.toml                 # Configuração do projeto (UV/Python)
    ├── uv.lock
    ├── requirements.txt               # Requisitos do Projeto
    │
    ├── model_train.py                 # Treinamento dos modelos
    ├── model_predict.py               # Predição usando embeddings + regex
    ├── web_scraping.py                # Script geral de scraping (atalho)
    ├── README.md
    │
    ├── data/
    │   ├── raw/
    │   │   ├── posts_com_labels.xlsx  # Dataset rotulado manualmente (Versão Antiga, Não é Mais Utilizado)
    │   │   ├── posts_linkedin.csv     # Dados brutos do scraper
    │   │   └── posts_treino.xlsx      # Dataset Utilizado no Treino
    │   │
    │   ├── processed/
    │   │   ├── posts_preditos.csv     # Resultado final das predições
    │   │   ├── treino_label.csv       # Dataset Criado pelo Modelo 1 durante o Treinamento
    │   │   └── treino_senioridade.csv # Dataset Criado pelo Modelo 2 durante o Treinamento
    │   │
    │   └── fixes/                     # Scripts auxiliares de manutenção
    │       ├── atualizar_senioridade.py
    │       ├── filtrar_e_juntar_datasets.py
    │       ├── padronizar_todas_datas.py
    │       └── teste_filtro_duplicatas.py
    │
    ├── graphs/
    │   ├── Dashboard.png              # Imagem do dashboard Power BI
    │   └── graficos.pbix              # Arquivo original do Power BI
    │
    ├── logs/                          # Logs do scraper / execuções
    │
    ├── models/
    │   ├── model_labels.pkl           # Modelo 1 (tipo do post)
    │   ├── model_sen.pkl              # Modelo 2 (senioridade)
    │   └── encoder_regex.pkl          # Encoder one-hot dos regex
    │
    └── src/
        ├── nlp/
        │   └── model_utils.py         # Embeddings, combine_embeddings, training utils
        │
        └── scraping/
            ├── post_scraper.py        # Função principal de scraping
            └── scraping_utils.py
                ├── cookies.json           # Cookies salvos do LinkedIn
                ├── cookies.py             # Gestão de cookies do scraper
                ├── csv_storage.py         # Salvamento incremental em CSV
                ├── driver_setup.py        # Configuração do Selenium WebDriver
                ├── extract_post_information.py # Parsing do HTML bruto
                ├── filtrar_posts_duplicados.py # Filtro de duplicação
                ├── post_filters.py        # Configura o filtro de busca
                ├── scrolling.py           # Lógica de scroll automático
                ├── text_cleaning.py       # Limpeza de texto + extração via regex
                └── waits.py               # Aguardos específicos do scraper

## 🕸️ 1. Coleta de Dados (LinkedIn)

A extração é feita com <strong>Selenium WebDriver</strong> e <strong>BeautifulSoup4</strong> que coletam:

    Autor
    
    Texto
    
    Hashtags
    
    Link da publicação
    
    Localização
    
    Data (incluindo datas relativas como “1 sem”, “há 3 h”)

Foi criada uma função completa que converte datas relativas em datas absolutas no formato YYYY-MM-DD.

## 🧼 2. Limpeza e Padronização

    Normalização de texto
    
    Remoção de HTML
    
    Padronização de datas
    
    Limpeza de hashtags
    
    Tratamento de campos vazios
    
    Unificação do formato textual do dataset

## 🧹 3. Deduplicação Avançada

O LinkedIn frequentemente repete vagas ou republica conteúdo quase idêntico.

O pipeline remove duplicações em duas etapas:

    1. Duplicatas exatas (texto + data)
    2. Similaridade TF-IDF (> 0.92)

Usando:

    TF-IDF Vectorizer
    
    Cosine Similarity
    
    Normalização textual

Resultado da deduplicação:

    Dataset original: 1264 posts
    95 removidos por texto+data
    163 removidos por similaridade (>0.92)
    Total removidos: 258
    Dataset final: 1006 posts únicos

## 🧠 4. Embeddings com Sentence-BERT

Modelo utilizado:

    sentence-transformers/all-MiniLM-L6-v2

Geramos embeddings para:

    autor
    
    texto
    
    hashtags

E concatenamos:

    X = [emb_author | emb_text | emb_hash]

## 🏷️ 5. Modelo 1 — Classificação do Tipo de Post

Classes:

    vaga
    
    postagem
    
    estrangeiro

Modelo: Logistic Regression

Resultados:

|Tipo|Precisão|Recall|F1-Score|
|:---:|:---:|:---:|:---:|
|Estrangeiro|0.90|0.79|0.84|
|Postagem|0.88|0.82|0.85|
|Vaga|0.88|0.94|0.91|

## 🎯 6. Modelo 2 — Classificação de Senioridade

Classes:

    Estagio
    
    Junior
    
    Pleno
    
    Senior

    Multi (Múltiplas Vagas na Postagem)

✔ Features utilizadas:

    embeddings (S-BERT)
    
    regex_onehot (junior/pleno/senior/estagio/multi)

Comparativo da performance após limpeza do dataset e inclusão do regex:

|Classe |F1 Antes|F1 Depois|Diferença|
|:---:|:---:|:---:|:---:|
|Estágio|0.00|0.83|+83 pontos|
|Júnior|0.34|0.61|+27 pontos|
|Pleno|0.53|0.70|+17 pontos|
|Sênior|0.33|0.77|+44 pontos
|Multi|0.84|0.77|-7 Pontos|           

## 🔮 7. Pipeline de Predição
O script model_predict.py:

    Carrega o modelo de embeddings

    Carrega os modelos de labels e senioridade

    Carrega o OneHotEncoder salvo no treinamento

    Gera embeddings + regex → one-hot

    Concatena embeddings e features

    Faz predição do tipo de post

    Se for vaga → predição da senioridade

    Salva em data/processed/posts_preditos.csv

## 📊 8. Dashboard Power BI

<img width="1431" height="805" alt="Dashboard" src="https://github.com/user-attachments/assets/0d3b1707-2211-4455-8ca2-142c582bec03" />

Inclui:

    Total de Posts

    Gráfico em Rosquinha da distribuição de tipos de posts
    
    Total de Vagas por Senioridade

    Tabela com Texto e Link das Vagas

    Total de Posts Por Data
    
    Hashtags mais presentes

Dataset utilizado: posts_preditos.csv.

## 🌐 9. Deploy no Portfólio (em construção)

A página do portfólio contará com input para colar o link de uma vaga

Endpoint Flask que:
    
    Recebe o link
    
    Roda scraping da vaga
    
    Limpa e normaliza texto
    
    Gera embeddings

    Prediz tipo + senioridade + probabilidade

    Retorna JSON para o front-end

Apresentação visual com:

    Tipo do post
    
    Senioridade prevista
      
    Hashtags
      
    Presencial/Híbrido/Remoto
      
    Storytelling do projeto
      
    Animações e gifs (scraping, embeddings, matrix, etc.)

## 🏁 10. Conclusão

Este projeto representa um pipeline completo e profissional de NLP, Web Scraping, Machine Learning e Deploy, reunindo:

    Engenharia de dados
    
    Limpeza e deduplicação inteligente
    
    Embeddings modernos
    
    Modelos de classificação multietapas
    
    Integração futura com página web
    
    Storytelling completo para portfólio
