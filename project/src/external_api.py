import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()  # читает .env и кладёт переменные в окружение

API_URL = "https://api.apilayer.com/exchangerates_data/convert"


def convert_to_rub(amount: float, currency: str) -> float:
    """Переводит сумму из USD или EUR в рубли через внешний API."""
    api_key = os.getenv("API_KEY")
    if api_key is None:
        raise ValueError("Не найден API_KEY в переменных окружения (.env)")

    response = requests.get(
        API_URL,
        headers={"apikey": api_key},
        params={"from": currency, "to": "RUB", "amount": amount},
        timeout=10,
    )
    response.raise_for_status()  # если сервер вернул ошибку, будет исключение

    return float(response.json()["result"])


def get_transaction_amount_rub(transaction: dict[str, Any]) -> float:
    """Возвращает сумму транзакции в рублях (float)."""
    operation = transaction["operationAmount"]
    amount = float(operation["amount"])
    currency = operation["currency"]["code"]

    if currency == "RUB":
        return amount
    if currency in ("USD", "EUR"):
        return convert_to_rub(amount, currency)

    raise ValueError(f"Неподдерживаемая валюта: {currency}")
