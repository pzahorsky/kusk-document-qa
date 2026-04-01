import json
from datetime import datetime, timezone
from pathlib import Path

LOG_FILE = Path("log/qa_log.json")

def logger(question, answer, sources):
    LOG_FILE.parent.mkdir(exist_ok = True)

    log = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "question": question,
        "answer": answer,
        "sources": sources
    }

    with open(LOG_FILE, "a", encoding = "utf-8") as f:
        f.write(json.dumps(log) + "\n")