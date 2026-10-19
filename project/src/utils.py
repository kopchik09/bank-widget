import json
from typing import Any


def load_transactions(path: str) -> list[dict[str, Any]]:
    """Читает транзакции из JSON-файла. При любой проблеме возвращает []."""
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    if not isinstance(data, list):
        return []

    return data
