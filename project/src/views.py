"""Функции формирования JSON-ответа для главной страницы."""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import requests

logger = logging.getLogger(__name__)
SETTINGS_PATH = Path("user_settings.json")
CURRENCY_API_URL = "https://open.er-api.com/v6/latest/USD"
STOCK_API_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"


def get_greeting(date_time: datetime) -> str:
    """Возвращает приветствие в зависимости от часа."""
    hour = date_time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    if 12 <= hour < 18:
        return "Добрый день"
    if 18 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def _amount(transaction: dict[str, Any]) -> float:
    """Достаёт сумму из поддерживаемых форматов транзакции."""
    value = transaction.get("amount")
    if value is None:
        value = transaction.get("operationAmount", {}).get("amount", 0)
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _date(transaction: dict[str, Any]) -> datetime | None:
    value = transaction.get("date") or transaction.get("Дата операции")
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value)[:19].replace("Z", ""))
    except ValueError:
        return None


def _description(transaction: dict[str, Any]) -> str:
    return str(transaction.get("description") or transaction.get("Описание") or "")


def _category(transaction: dict[str, Any]) -> str:
    return str(transaction.get("category") or transaction.get("Категория") or "")


def _card_digits(transaction: dict[str, Any]) -> str | None:
    source = str(transaction.get("from") or transaction.get("Номер карты") or "")
    # В переводах со счёта номер счёта не считается банковской картой.
    if not source or "счет" in source.lower() or "счёт" in source.lower():
        return None
    digits = "".join(character for character in source if character.isdigit())
    return digits[-4:] if len(digits) >= 4 else None


def load_user_settings(path: str | Path = SETTINGS_PATH) -> dict[str, list[str]]:
    """Загружает пользовательские валюты и акции; при ошибке использует пустые списки."""
    try:
        with open(path, encoding="utf-8") as file:
            settings = json.load(file)
        return {
            "user_currencies": settings.get("user_currencies", []),
            "user_stocks": settings.get("user_stocks", []),
        }
    except (OSError, json.JSONDecodeError, AttributeError):
        logger.warning("Не удалось прочитать пользовательские настройки из %s", path)
        return {"user_currencies": [], "user_stocks": []}


def get_currency_rates(currencies: list[str]) -> list[dict[str, Any]]:
    """Получает курсы валют относительно рубля; при недоступности API возвращает []."""
    if not currencies:
        return []
    try:
        response = requests.get(CURRENCY_API_URL, timeout=5)
        response.raise_for_status()
        rates = response.json().get("rates", {})
        usd_to_rub = rates.get("RUB")
        if not usd_to_rub:
            return []
        result = []
        for currency in currencies:
            if currency.upper() == "USD":
                rate = usd_to_rub
            else:
                rate = rates.get(currency.upper())
                # API возвращает число единиц валюты за USD; пересчитываем в RUB.
                if rate:
                    rate = usd_to_rub / rate
            if rate:
                result.append({"currency": currency.upper(), "rate": round(float(rate), 2)})
        return result
    except (requests.RequestException, ValueError, TypeError, KeyError) as error:
        logger.warning("Не удалось получить курсы валют: %s", error)
        return []


def get_stock_prices(stocks: list[str]) -> list[dict[str, Any]]:
    """Получает последние доступные цены акций через Yahoo Finance chart API."""
    result = []
    for stock in stocks:
        try:
            response = requests.get(
                STOCK_API_URL.format(symbol=stock), timeout=5,
                headers={"User-Agent": "Mozilla/5.0"},
            )
            response.raise_for_status()
            quote = response.json()["chart"]["result"][0]["indicators"]["quote"][0]["close"]
            prices = [price for price in quote if price is not None]
            if prices:
                result.append({"stock": stock, "price": round(float(prices[-1]), 2)})
        except (requests.RequestException, ValueError, TypeError, KeyError, IndexError) as error:
            logger.warning("Не удалось получить цену акции %s: %s", stock, error)
    return result


def main_page(date_time: str, transactions: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Формирует данные главной страницы за начало месяца по указанную дату.

    Данные передаются аргументом, поэтому бизнес-логика не зависит от файла.
    """
    try:
        selected_date = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    except ValueError as error:
        raise ValueError("Дата должна иметь формат YYYY-MM-DD HH:MM:SS") from error

    start_date = selected_date.replace(day=1, hour=0, minute=0, second=0)
    period = []
    for transaction in transactions:
        transaction_date = _date(transaction)
        if transaction_date and start_date <= transaction_date <= selected_date:
            period.append(transaction)

    cards: dict[str, float] = {}
    for transaction in period:
        digits = _card_digits(transaction)
        if digits:
            cards[digits] = cards.get(digits, 0.0) + abs(_amount(transaction))

    cards_data = [
        {
            "last_digits": digits,
            "total_spent": round(total, 2),
            "cashback": round(total // 100, 2),
        }
        for digits, total in sorted(cards.items())
    ]
    top_transactions = sorted(period, key=lambda item: abs(_amount(item)), reverse=True)[:5]
    top_data = []
    for transaction in top_transactions:
        transaction_date = _date(transaction)
        top_data.append({
            "date": transaction_date.strftime("%d.%m.%Y") if transaction_date else "",
            "amount": round(_amount(transaction), 2),
            "category": _category(transaction),
            "description": _description(transaction),
        })

    settings = load_user_settings()
    return {
        "greeting": get_greeting(selected_date),
        "cards": cards_data,
        "top_transactions": top_data,
        "currency_rates": get_currency_rates(settings["user_currencies"]),
        "stock_prices": get_stock_prices(settings["user_stocks"]),
    }


# Понятное имя для вызова из других модулей.
def get_main_page(date_time: str, transactions: list[dict[str, Any]]) -> dict[str, Any]:
    return main_page(date_time, transactions)
