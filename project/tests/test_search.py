from typing import Any

from src.search import process_bank_operations, process_bank_search

DATA: list[dict[str, Any]] = [
    {"id": 1, "description": "Перевод организации"},
    {"id": 2, "description": "Открытие вклада"},
    {"id": 3, "description": "Перевод со счета на счет"},
    {"id": 4, "description": "Перевод с карты на карту"},
    {"id": 5},  # нет описания
]


def test_search_finds_matches() -> None:
    result = process_bank_search(DATA, "вклад")

    assert [operation["id"] for operation in result] == [2]


def test_search_is_case_insensitive() -> None:
    result = process_bank_search(DATA, "ПЕРЕВОД")

    assert [operation["id"] for operation in result] == [1, 3, 4]


def test_search_no_matches() -> None:
    assert process_bank_search(DATA, "кредит") == []


def test_search_special_characters_are_literal() -> None:
    data = [{"description": "Оплата (услуги)"}, {"description": "Оплата услуг"}]

    # "." и "(" не должны работать как части регулярного выражения
    assert process_bank_search(data, ".") == []
    assert process_bank_search(data, "(услуги)") == [data[0]]


def test_search_skips_operations_without_description() -> None:
    assert process_bank_search([{"id": 5}, {"description": None}], "перевод") == []


def test_search_empty_data() -> None:
    assert process_bank_search([], "перевод") == []


def test_operations_counts_categories() -> None:
    categories = ["Перевод организации", "Открытие вклада"]

    assert process_bank_operations(DATA, categories) == {
        "Перевод организации": 1,
        "Открытие вклада": 1,
    }


def test_operations_counts_repeated_category() -> None:
    data = [{"description": "Перевод"}, {"description": "Перевод"}, {"description": "Вклад"}]

    assert process_bank_operations(data, ["Перевод"]) == {"Перевод": 2}


def test_operations_missing_category_is_zero() -> None:
    assert process_bank_operations(DATA, ["Кредит"]) == {"Кредит": 0}


def test_operations_ignores_other_categories() -> None:
    result = process_bank_operations(DATA, ["Открытие вклада"])

    assert list(result) == ["Открытие вклада"]


def test_operations_empty_data() -> None:
    assert process_bank_operations([], ["Перевод"]) == {"Перевод": 0}


def test_operations_empty_categories() -> None:
    assert process_bank_operations(DATA, []) == {}
