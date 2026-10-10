import pytest
from project.src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "number, expected",
    [
        ("1234567890123456", "1234 56** **** 3456"),
        ("0000000000000000", "0000 00** **** 0000"),
        ("1111112222223333", "1111 11** **** 3333"),
    ],
)
def test_get_mask_card_number(number, expected):
    assert get_mask_card_number(number) == expected


def test_get_mask_card_number_invalid_uses_new_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda: "1234567890123456")
    assert get_mask_card_number("123") == (
        "Напишите номер счета правильно/n 1234 56** **** 3456"
    )


@pytest.mark.parametrize(
    "number, expected",
    [
        ("1234567890123456", "**3456"),
        ("0000000000000000", "**0000"),
        ("9999999999999999", "**9999"),
    ],
)
def test_get_mask_account(number, expected):
    assert get_mask_account(number) == expected


def test_get_mask_account_invalid_uses_new_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda: "1234567890123456")
    assert get_mask_account("123") == "Напишите номер счета правильно/n **3456"
