# Document QA Tool

Projekt implementuje jednoduchý nástroj pre vyhľadávanie informacií v dokumentov pomocou LLM.

## Popis funkcie

Aplikácia načíta PDF dokumenty, spracuje ich do vektorovej databázy a umožňuje klásť otázky v prirodzenom jazyku. Odpovede sú generované výhradne z obsahu načítaných dokumentov a obsahujú referencie na zdroje.

## Architekúra

- **app.py** - Hlavná aplikácia s CLI rozhraním pre kladenie otázok
- **rag_pipeline.py** - Načítanie PDF súborov, chunking, práca s vektorou DB
- **llm.py** - Embeddings a odpovede z LLM
- **logger.py** - Logovanie otázok a odpovedí
- **chroma_db/** - Uložená vektorová DB
- **data/** - Dáta (Zmluvy)
- **index/** - Evidencia spracovaných dokumentov
- **test_questions.json** - Sada Testovacích otázok a odpovedí

## Technológie

- Python
- OpenAI API (Embeddings + LLM)
- PyMuPDF (Spracovanie PDF)
- ChromaDB (Vektorová DB)
- python-dotenv (API key)
- JSON (ukladanie konfigurácií a logov)
- pathlib (práca so súbormi a cesty)
- datetime (timestamps v logoch)

## Spustenie

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Poznámky

V projekte sú použité textové PDF dokumenty. Skenované dokumenty neboli zahrnuté aby nebolo nutné implementovať OCR.
