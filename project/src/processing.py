def filter_by_state(transactions, state="EXECUTED"):
    """
    Возвращает список транзакций с указанным статусом.

    Args:
        transactions: Список словарей с данными о транзакциях.
        state: Значение поля "state" для фильтрации. По умолчанию "EXECUTED".

    Returns:
        Список транзакций, у которых поле "state" совпадает с переданным значением.
    """
    return [i for i in transactions if i.get("state") == state]


def sort_by_date(transactions, method=True):
    """
    Сортирует список транзакций по дате в формате ISO (YYYY-MM-DD...).

    Дата хранится как строка; сортировка выполняется лексикографически.
    Для ISO-формата это эквивалентно хронологической сортировке.

    Args:
        transactions: Список словарей с данными о транзакциях.
        reverse: Если True, сортировка по убыванию (новые сначала). По умолчанию False.

    Returns:
        Новый список транзакций, отсортированный по полю "date".
    """
    return sorted(transactions, key=lambda x: x["date"], reverse=method)


# пример списка словарей
lists = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]


if __name__ == "__main__":
    # print(sort_by_date(lists))
    print(filter_by_state(lists))
