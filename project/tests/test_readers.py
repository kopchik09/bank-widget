import csv
from pathlib import Path
from typing import Any

from openpyxl import Workbook

from src.readers import read_csv, read_xlsx

HEADER = [
    "id", "state", "date", "amount", "currency_name", "currency_code", "from", "to", "description",
]
ROWS: list[list[Any]] = [
    [1, "EXECUTED", "2019-12-08T22:46:21", "40542", "Russian Ruble", "RUB", "",
     "Счет 90424923579946435907", "Открытие вклада"],
    [2, "PENDING", "2019-11-12T20:30:00", "130", "US Dollar", "USD",
     "MasterCard 7771270000003727", "Visa Platinum 1293380000009203", "Перевод с карты на карту"],
]


def make_csv(path: Path) -> None:
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(HEADER)
        writer.writerows(ROWS)


def make_xlsx(path: Path, rows: list[list[Any]] = ROWS) -> None:
    workbook = Workbook()
    sheet = workbook.active
    assert sheet is not None
    sheet.append(HEADER)
    for row in rows:
        sheet.append(row)
    workbook.save(path)


def test_read_csv_converts_rows(tmp_path: Path) -> None:
    file = tmp_path / "ops.csv"
    make_csv(file)

    result = read_csv(str(file))

    assert len(result) == 2
    assert result[1] == {
        "id": "2",
        "state": "PENDING",
        "date": "2019-11-12T20:30:00",
        "operationAmount": {
            "amount": "130",
            "currency": {"name": "US Dollar", "code": "USD"},
        },
        "description": "Перевод с карты на карту",
        "from": "MasterCard 7771270000003727",
        "to": "Visa Platinum 1293380000009203",
    }


def test_read_csv_empty_source_becomes_none(tmp_path: Path) -> None:
    file = tmp_path / "ops.csv"
    make_csv(file)

    assert read_csv(str(file))[0]["from"] is None


def test_read_csv_file_not_found(tmp_path: Path) -> None:
    assert read_csv(str(tmp_path / "no_such_file.csv")) == []


def test_read_csv_empty_file(tmp_path: Path) -> None:
    file = tmp_path / "ops.csv"
    file.write_text("", encoding="utf-8")

    assert read_csv(str(file)) == []


def test_read_xlsx_converts_rows(tmp_path: Path) -> None:
    file = tmp_path / "ops.xlsx"
    make_xlsx(file)

    result = read_xlsx(str(file))

    assert len(result) == 2
    assert result[0]["state"] == "EXECUTED"
    assert result[0]["operationAmount"]["currency"]["code"] == "RUB"
    assert result[0]["description"] == "Открытие вклада"
    assert result[0]["from"] is None
    assert result[0]["to"] == "Счет 90424923579946435907"


def test_read_xlsx_numeric_amount_becomes_string(tmp_path: Path) -> None:
    file = tmp_path / "ops.xlsx"
    make_xlsx(file, [[1, "EXECUTED", "2019-12-08T22:46:21", 40542.5, "Ruble", "RUB", "", "", "Вклад"]])

    assert read_xlsx(str(file))[0]["operationAmount"]["amount"] == "40542.5"


def test_read_xlsx_only_header(tmp_path: Path) -> None:
    file = tmp_path / "ops.xlsx"
    make_xlsx(file, [])

    assert read_xlsx(str(file)) == []


def test_read_xlsx_file_not_found(tmp_path: Path) -> None:
    assert read_xlsx(str(tmp_path / "no_such_file.xlsx")) == []


def test_read_xlsx_broken_file(tmp_path: Path) -> None:
    file = tmp_path / "ops.xlsx"
    file.write_text("это не настоящий xlsx", encoding="utf-8")

    assert read_xlsx(str(file)) == []
