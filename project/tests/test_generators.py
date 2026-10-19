import pytest

from project.src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)

# ---------------------------------------------------------------------------
# filter_by_currency
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "code, expected_ids",
    [
        ("USD", [939719570, 142264268, 895315941]),
        ("RUB", [873106923, 594226727]),
    ],
)
def test_filter_by_currency_codes(transactions_generator, code, expected_ids):
    result = filter_by_currency(transactions_generator, code)
    assert [item["id"] for item in result] == expected_ids


def test_filter_by_currency_returns_same_objects(transactions_generator):
    result = list(filter_by_currency(transactions_generator, "USD"))
    assert result == [transactions_generator[0], transactions_generator[1], transactions_generator[3]]


def test_filter_by_currency_is_generator(transactions_generator):
    result = filter_by_currency(transactions_generator, "USD")
    # next() должен работать -> перед нами генератор, а не список
    first = next(result)
    assert first["id"] == 939719570
    second = next(result)
    assert second["id"] == 142264268


def test_filter_by_currency_missing_currency_field_is_skipped():
    data = [
        {"id": 1, "operationAmount": {"amount": "10.00"}},  # нет currency
        {"id": 2},  # нет operationAmount вообще
        {
            "id": 3,
            "operationAmount": {"currency": {"code": "USD"}},
        },
    ]
    result = list(filter_by_currency(data, "USD"))
    assert [item["id"] for item in result] == [3]


def test_filter_by_currency_empty_list():
    assert list(filter_by_currency([], "USD")) == []


# ---------------------------------------------------------------------------
# transaction_descriptions
# ---------------------------------------------------------------------------

def test_transaction_descriptions_full_list(transactions_generator):
    result = list(transaction_descriptions(transactions_generator))
    assert result == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]


def test_transaction_descriptions_is_generator(transactions_generator):
    gen = transaction_descriptions(transactions_generator)
    assert next(gen) == "Перевод организации"
    assert next(gen) == "Перевод со счета на счет"


def test_transaction_descriptions_missing_field_returns_none():
    data = [{"id": 1}]
    result = list(transaction_descriptions(data))
    assert result == [None]


def test_transaction_descriptions_empty_list():
    assert list(transaction_descriptions([])) == []


# ---------------------------------------------------------------------------
# card_number_generator
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "start, end, expected",
    [
        (1, 5, [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005",
        ]),
        (10, 10, ["0000 0000 0000 0010"]),
        (9999999999999999, 9999999999999999, ["9999 9999 9999 9999"]),
    ],
)
def test_card_number_generator_values(start, end, expected):
    assert list(card_number_generator(start, end)) == expected
