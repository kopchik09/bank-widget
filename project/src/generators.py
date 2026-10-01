"""
Модуль generators.py

Содержит функции-генераторы для обработки данных о транзакциях:
- filter_by_currency: фильтрация транзакций по валюте.
- transaction_descriptions: последовательный вывод описаний операций.
- card_number_generator: генерация номеров банковских карт в заданном диапазоне.
"""

from typing import Dict, Iterator, List


def filter_by_currency(
    transactions: List[Dict], currency: str
) -> Iterator[Dict]:
    """
    Принимает список словарей с транзакциями и код валюты.
    Возвращает итератор, поочерёдно выдающий транзакции,
    у которых валюта операции совпадает с заданной.

    :param transactions: список словарей с данными о транзакциях.
    :param currency: код валюты, например "USD".
    :return: итератор транзакций с указанной валютой.
    """
    for transaction in transactions:
        operation_currency = (
            transaction.get("operationAmount", {})
            .get("currency", {})
            .get("code")
        )
        if operation_currency == currency:
            yield transaction


def transaction_descriptions(transactions: List[Dict]) -> Iterator[str]:
    """
    Принимает список словарей с транзакциями.
    Возвращает генератор, поочерёдно выдающий описание
    каждой операции (значение ключа "description").

    :param transactions: список словарей с данными о транзакциях.
    :return: генератор строк с описаниями операций.
    """
    for transaction in transactions:
        yield transaction.get("description")


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генерирует номера банковских карт в формате
    "XXXX XXXX XXXX XXXX" для диапазона чисел от start до end включительно.

    Допустимый диапазон значений: от 1 до 9999 9999 9999 9999.

    :param start: начальное значение диапазона.
    :param end: конечное значение диапазона.
    :return: генератор строк — номеров карт.
    """
    for number in range(start, end + 1):
        digits = f"{number:016d}"
        yield " ".join(
            digits[i : i + 4] for i in range(0, len(digits), 4)
        )


if __name__ == "__main__":
    # Небольшая демонстрация работы генераторов
    transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
    ]

    usd_transactions = filter_by_currency(transactions, "USD")
    for _ in range(2):
        print(next(usd_transactions))

    descriptions = transaction_descriptions(transactions)
    for _ in range(2):
        print(next(descriptions))

    for card_number in card_number_generator(1, 5):
        print(card_number)
