import pytest
from project.src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "value, expected",
    [
        ("Visa 1234567890123456", "Visa 1234 56** **** 3456"),
        ("MasterCard 1111222233334444", "MasterCard 1111 22** **** 4444"),
        ("МИР 9999999999999999", "МИР 9999 99** **** 9999"),
    ],
)
def test_mask_account_card_cards(value, expected):
    assert mask_account_card(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("Счет 1234567890123456", "Счет **3456"),
        ("Счет 35383033474447895560", "Счет **5560"),
    ],
)
def test_mask_account_card_accounts(value, expected):
    assert mask_account_card(value) == expected


def test_mask_account_card_empty_raises():
    with pytest.raises(IndexError):
        mask_account_card("")


@pytest.mark.parametrize(
    "value, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2019-07-03T18:35:29.512364", "03.07.2019"),
        ("2000-01-01", "01.01.2000"),
    ],
)
def test_get_date(value, expected):
    assert get_date(value) == expected


@pytest.mark.parametrize("value", ["", "2024", "abc", "01.02.2024"])
def test_get_date_short_or_nonstandard(value):
    # Функция не валидирует дату, а берёт символы по фиксированным позициям.
    expected_values = {
        "": "..",
        "2024": "..2024",
        "abc": "..abc",
        "01.02.2024": "24..2.01.0",
    }
    assert get_date(value) == expected_values[value]
