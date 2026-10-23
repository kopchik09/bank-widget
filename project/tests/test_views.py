from src import views


def test_get_greeting():
    from datetime import datetime

    assert views.get_greeting(datetime(2024, 1, 1, 8)) == "Доброе утро"
    assert views.get_greeting(datetime(2024, 1, 1, 14)) == "Добрый день"
    assert views.get_greeting(datetime(2024, 1, 1, 20)) == "Добрый вечер"
    assert views.get_greeting(datetime(2024, 1, 1, 2)) == "Доброй ночи"


def test_main_page_aggregates_cards_and_top_transactions(monkeypatch, tmp_path):
    monkeypatch.setattr(views, "SETTINGS_PATH", tmp_path / "missing.json")
    monkeypatch.setattr(views, "get_currency_rates", lambda currencies: [])
    monkeypatch.setattr(views, "get_stock_prices", lambda stocks: [])
    transactions = [
        {
            "date": "2024-05-02T10:00:00",
            "amount": -250,
            "from": "Visa 12345678",
            "description": "Магазин",
            "category": "Продукты",
        },
        {
            "date": "2024-05-10T10:00:00",
            "amount": -80,
            "from": "Visa 12345678",
            "description": "Кофе",
            "category": "Кафе",
        },
        {
            "date": "2024-04-30T10:00:00",
            "amount": -10000,
            "from": "Visa 12345678",
            "description": "Старый платёж",
            "category": "Другое",
        },
    ]

    result = views.main_page("2024-05-31 23:00:00", transactions)

    assert result["greeting"] == "Доброй ночи"
    assert result["cards"] == [{"last_digits": "5678", "total_spent": 330.0, "cashback": 3.0}]
    assert len(result["top_transactions"]) == 2
    assert result["top_transactions"][0]["description"] == "Магазин"


def test_main_page_invalid_date():
    import pytest

    with pytest.raises(ValueError):
        views.main_page("31-05-2024", [])
