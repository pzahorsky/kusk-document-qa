import rag_pipeline as rag
import llm

documents = rag.pdf_folder_loader("data/")

collection = rag.init_vector_storage()
print(collection.count())

rag.store_chunks(documents, collection)

while True:
    question = input("\nZadaj otázku ('exit' pre koniec):")

    if question == "exit":
        break

    question_embedding = llm.get_embeddings(question)

    response = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )

    print(response["documents"][0])