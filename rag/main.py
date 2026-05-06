from rag.ingestion.index_builder import build_index
from rag.chains.qa_chain import build_qa_chain

def run():
    print("1. Build index")
    print("2. Ask questions")

    choice = input("Enter choice: ")

    if choice == "1":
        build_index()

    elif choice == "2":
        qa = build_qa_chain()

        while True:
            query = input("Ask: ")
            if query == "exit":
                break

            result = qa.run(query)
            print("\nAnswer:", result)


if __name__ == "__main__":
    run()