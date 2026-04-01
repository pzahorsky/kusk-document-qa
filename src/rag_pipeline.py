import fitz as pdf
from pathlib import Path
import chromadb
from llm import get_embeddings
import json
from pathlib import Path

INDEX_FILE = Path("index/indexed_files.json")

def pdf_folder_loader(folder_path: str, index_file = INDEX_FILE):
    documents = []
    newly_processed = []

    index_file.parent.mkdir(exist_ok = True)

    if index_file.exists():
        index_files = json.loads(index_file.read_text(encoding = "utf-8"))
    else:
        index_files = []

    for file in Path(folder_path).glob("*.pdf"):
        if file.name in index_files:
            continue

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
        newly_processed.append(file.name)
    
    return documents, newly_processed

def init_vector_storage():
    database = chromadb.PersistentClient(path = "./chroma_db")
    collection = database.get_or_create_collection(name = "contracts")

    return collection

def store_chunks(documents, collection):
    try:
        for index, document in enumerate(documents):
            embedding = get_embeddings(document["text"])

            collection.add(
                ids = [f"chunk_{index}"],
                documents = [document["text"]],
                metadatas = [document["metadata"]],
                embeddings = [embedding]
            )
        return True
    
    except Exception as e:
        print(f"Error saving to DB: {e}")
        return False

def index_saved_info(new_files, index_file = INDEX_FILE):
    index_file.parent.mkdir(exist_ok = True)

    if index_file.exists():
        index_files = json.loads(index_file.read_text(encoding = "utf-8"))
    else:
        index_files = []

    for file in new_files:
        if file not in index_files:
            index_files.append(file)

    index_file.write_text(
        json.dumps(index_files, indent = 2, ensure_ascii = False),
        encoding = "utf-8"
    )