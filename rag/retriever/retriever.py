from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

def get_retriever():
    embeddings = OllamaEmbeddings(model="mistral")

    vectordb = Chroma(persist_directory="rag/chroma_db", embedding_function=embeddings)

    return vectordb.as_retriever(search_kwargs={"k": 5})
