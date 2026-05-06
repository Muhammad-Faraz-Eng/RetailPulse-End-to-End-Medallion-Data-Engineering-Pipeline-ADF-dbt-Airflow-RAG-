import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

load_dotenv(dotenv_path="docker/.env")


def get_engine():
    conn_str = (
        f"mssql+pyodbc://{os.getenv('AZURE_SQL_USER')}:{os.getenv('AZURE_SQL_PASSWORD')}"
        f"@{os.getenv('AZURE_SQL_SERVER')}:1433/{os.getenv('AZURE_SQL_DATABASE')}"
        "?driver=ODBC+Driver+17+for+SQL+Server"
    )

    return create_engine(conn_str)


def extract_data():
    engine = get_engine()

    queries = {
        "sales": "SELECT TOP 100 * FROM fact_sales",
        "products": "SELECT * FROM dim_product",
        "currency": "SELECT * FROM dim_currency",
    }
    data = {}

    for name, query in queries.items():
        data[name] = pd.read_sql(query, engine)

    return data


def dataframe_to_docs(df, source_name):
    docs = []

    for _, row in df.iterrows():
        content = ", ".join([f"{col}" for col in df.columns])

        docs.append(
            Document(
                page_content=content,
                metadata={"Source": source_name},
            )
        )

    return docs


def build_index():
    data = extract_data()

    all_docs = []

    for name, df in data.items():
        docs = dataframe_to_docs(df, name)
        all_docs.extend(docs)

    embeddings = OllamaEmbeddings(model="mistral")

    vectordb = Chroma.from_documents(
        documents=all_docs,
        embedding=embeddings,
        persist_directory="rag/chroma_db",
    )

    vectordb.persist()

    print("Index Built Successfully")
