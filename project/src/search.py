import re
from collections import Counter
from typing import Any


def process_bank_search(data: list[dict[str, Any]], search: str) -> list[dict[str, Any]]:
    """
    Возвращает операции, в описании которых встречается строка поиска.

    Поиск идёт через модуль re без учёта регистра. Строка поиска
    экранируется (re.escape), поэтому символы вроде "." или "(" ищутся
    как обычный текст, а не как части регулярного выражения.
    """
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [
        operation
        for operation in data
        if pattern.search(str(operation.get("description") or ""))
    ]


def process_bank_operations(data: list[dict[str, Any]], categories: list[str]) -> dict[str, int]:
    """
    Считает, сколько операций относится к каждой категории.

    Категория хранится в поле "description". В результат попадают все
    переданные категории, даже если операций в них нет (тогда значение 0).
    """
    counter = Counter(str(operation.get("description") or "") for operation in data)
    return {category: counter[category] for category in categories}
