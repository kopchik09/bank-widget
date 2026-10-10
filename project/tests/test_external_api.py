from unittest.mock import Mock, patch

import pytest

from src.external_api import API_URL, convert_to_rub, get_transaction_amount_rub


def make_transaction(amount: str, code: str) -> dict:
    return {"operationAmount": {"amount": amount, "currency": {"code": code}}}


def test_rub_transaction_does_not_call_api() -> None:
    with patch("src.external_api.requests.get") as mock_get:
        result = get_transaction_amount_rub(make_transaction("100.5", "RUB"))

    assert result == 100.5
    mock_get.assert_not_called()  # для рублей в API ходить не нужно


@patch("src.external_api.requests.get")
def test_usd_transaction_is_converted(mock_get: Mock, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_KEY", "test_key")
    mock_get.return_value.json.return_value = {"result": 9000.0}

    result = get_transaction_amount_rub(make_transaction("100", "USD"))

    assert result == 9000.0
    mock_get.assert_called_once_with(
        API_URL,
        headers={"apikey": "test_key"},
        params={"from": "USD", "to": "RUB", "amount": 100.0},
        timeout=10,
    )


@patch("src.external_api.requests.get")
def test_eur_transaction_is_converted(mock_get: Mock, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_KEY", "test_key")
    mock_get.return_value.json.return_value = {"result": 10000.0}

    assert get_transaction_amount_rub(make_transaction("100", "EUR")) == 10000.0


def test_unsupported_currency() -> None:
    with pytest.raises(ValueError):
        get_transaction_amount_rub(make_transaction("100", "JPY"))


def test_convert_without_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("API_KEY", raising=False)

    with pytest.raises(ValueError):
        convert_to_rub(100.0, "USD")
