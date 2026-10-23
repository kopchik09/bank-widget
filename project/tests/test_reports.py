import json

import pandas as pd

from src.reports import save_report, spending_by_category


def test_spending_by_category_filters_three_months(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    data = pd.DataFrame([
        {"Дата операции": "2024-05-01", "Категория": "Продукты", "Сумма операции": -100},
        {"Дата операции": "2024-02-01", "Категория": "Продукты", "Сумма операции": -200},
        {"Дата операции": "2024-04-01", "Категория": "Кафе", "Сумма операции": -300},
        {"Дата операции": "2023-12-01", "Категория": "Продукты", "Сумма операции": -400},
    ])

    result = spending_by_category(data, "продукты", "2024-05-01")

    assert result["Сумма операции"].tolist() == [-100, -200]
    assert (tmp_path / "report.json").exists()


def test_custom_report_filename(tmp_path):
    filename = tmp_path / "custom.json"

    @save_report(filename=str(filename))
    def report():
        return {"ok": True}

    assert report() == {"ok": True}
    assert json.loads(filename.read_text(encoding="utf-8")) == {"ok": True}
