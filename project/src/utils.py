import json
import logging
from pathlib import Path
from typing import Any

LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOGS_DIR / "utils.log", mode="w", encoding="utf-8")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)


def load_transactions(path: str) -> list[dict[str, Any]]:
    """Читает транзакции из JSON-файла. При любой проблеме возвращает []."""
    logger.info("Загрузка транзакций из файла %s", path)

    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        logger.error("Файл не найден: %s", path)
        return []
    except json.JSONDecodeError:
        logger.error("Файл пустой или содержит некорректный JSON: %s", path)
        return []

    if not isinstance(data, list):
        logger.error("В файле %s лежит не список, а %s", path, type(data).__name__)
        return []

    logger.info("Загружено транзакций: %d", len(data))
    return data