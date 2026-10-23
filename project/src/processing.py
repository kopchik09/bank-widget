from typing import Any


def filter_by_state(
    transactions: list[dict[str, Any]], state: str = "EXECUTED"
) -> list[dict[str, Any]]:
    """
    Возвращает список транзакций с указанным статусом.

    Args:
        transactions: Список словарей с данными о транзакциях.
        state: Значение поля "state" для фильтрации. По умолчанию "EXECUTED".

    Returns:
        Список транзакций, у которых поле "state" совпадает с переданным значением.
    """
    return [i for i in transactions if i.get("state") == state]


def sort_by_date(
    transactions: list[dict[str, Any]], method: bool = True
) -> list[dict[str, Any]]:
    """
    Сортирует список транзакций по дате в формате ISO (YYYY-MM-DD...).

    Дата хранится как строка; для ISO-формата лексикографическая сортировка
    совпадает с хронологической.

    Args:
        transactions: Список словарей с данными о транзакциях.
        method: True — по убыванию (новые сначала), False — по возрастанию.

    Returns:
        Новый список транзакций, отсортированный по полю "date".
    """
    return sorted(transactions, key=lambda x: str(x.get("date", "")), reverse=method)
