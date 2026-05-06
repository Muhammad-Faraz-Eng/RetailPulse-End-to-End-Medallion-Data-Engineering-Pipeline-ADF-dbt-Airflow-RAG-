from langchain_ollama import OllamaLLM
from rag.retriever.retriever import get_retriever


class SimpleQAChain:
    def __init__(self, llm, retriever):
        self.llm = llm
        self.retriever = retriever

    def run(self, query: str) -> str:
        docs = self.retriever.invoke(query)
        context = "\n\n".join([d.page_content for d in docs])

        prompt = (
            "Use the following context to answer the question concisely.\n\n"
            f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
        )

        # Ollama LLM provides a synchronous `invoke` method that returns text
        return self.llm.invoke(prompt)


def build_qa_chain():
    llm = OllamaLLM(model="mistral")
    retriever = get_retriever()
    return SimpleQAChain(llm, retriever)
