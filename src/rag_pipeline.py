import fitz as pdf
from pathlib import Path
import chromadb
from llm import get_embeddings

"""
Load data from the path and chunk the text by page.
"""
def pdf_folder_loader(folder_path: str):
    documents = []

    for file in Path(folder_path).glob("*.pdf"):
        doc = pdf.open(file)

        for page_num, page in enumerate(doc):
            text = page.get_text()

            if text.strip():
                documents.append(
                    {
                        "text": text,
                        "metadata": {
                            "source": file.name,
                            "page": page_num + 1
                        }
                })
    
    return documents

def init_vector_storage():
    database = chromadb.PersistentClient(path = "./chroma_db")
    collection = database.get_or_create_collection(name = "contracts")

    return collection

def store_chunks(documents, collection):
    for index, document in enumerate(documents):
        embedding = get_embeddings(document["text"])

        collection.add(
            ids = [f"chunk_{index}"],
            documents = [document["text"]],
            metadatas = [document["metadata"]],
            embeddings = [embedding]
        )

