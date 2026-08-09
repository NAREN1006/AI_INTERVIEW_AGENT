import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"


def load_curriculum():
    file_path = DOCS_DIR / "curriculum.json"

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_candidates():
    file_path = DOCS_DIR / "candidates.json"

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)