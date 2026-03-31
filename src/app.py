import rag_pipeline as rag
import llm

data = rag.pdf_folder_loader("data/")

collection = rag.init_vector_storage()

rag.store_chunks(data, collection)

while True:
    question = input("\nZadaj otázku ('exit' pre koniec):")

    if question == "exit":
        break

    question_embedding = llm.get_embeddings(question)

    retrieval_db = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )

    documents = retrieval_db["documents"][0]
    metadata = retrieval_db["metadatas"][0]

    context = "\n\n".join(documents)

    response = llm.answer_question(question, context)
    print(response)
    
    for document, meta in zip(documents, metadata):
        print(f"\n[{meta["source"]} - strana {meta["page"]}]")
