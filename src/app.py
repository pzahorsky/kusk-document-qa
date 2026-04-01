import rag_pipeline as rag
import llm
import logger as log

data, new_files = rag.pdf_folder_loader("data/")

collection = rag.init_vector_storage()

if new_files:
    stored = rag.store_chunks(data, collection)

    if stored:
        rag.index_saved_info(new_files)
else:
    print("Žiadne nové súbory na spracovanie")

while True:
    question = input("\nZadaj otázku ('exit' pre koniec):")

    if question == "exit":
        break

    question_embedding = llm.get_embeddings(question)

    retrieval_db = collection.query(
        query_embeddings=[question_embedding],
        n_results=2
    )

    documents = retrieval_db["documents"][0]
    metadata = retrieval_db["metadatas"][0]

    context = "\n\n".join(documents)

    response = llm.answer_question(question, context)
    print(response)
    
    for document, meta in zip(documents, metadata):
        sources = [
            {
                "source": meta['source'],
                "page": meta['page']
            }
        ]

        print(f"[{meta['source']} - strana {meta['page']}]")

    log.logger(question, response, sources)
