"""Тесты функций чтения файлов с транзакциями."""

from unittest.mock import Mock, patch

from project.src.readers import read_csv, read_excel


@patch("project.src.readers.pd.read_csv")
def test_read_csv_returns_transaction_records(mock_read_csv: Mock) -> None:
    """CSV-файл читается через pandas и преобразуется в список словарей."""
    expected_transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
    ]
    dataframe = Mock()
    dataframe.to_dict.return_value = expected_transactions
    mock_read_csv.return_value = dataframe

    result = read_csv("data/transactions.csv")

    assert result == expected_transactions
    mock_read_csv.assert_called_once_with("data/transactions.csv", delimiter=";")
    dataframe.to_dict.assert_called_once_with(orient="records")


@patch("project.src.readers.pd.read_excel")
def test_read_excel_returns_transaction_records(mock_read_excel: Mock) -> None:
    """Excel-файл читается через pandas и преобразуется в список словарей."""
    expected_transactions = [
        {"id": 3, "state": "PENDING"},
        {"id": 4, "state": "EXECUTED"},
    ]
    dataframe = Mock()
    dataframe.to_dict.return_value = expected_transactions
    mock_read_excel.return_value = dataframe

    result = read_excel("data/transactions_excel.xlsx")

    assert result == expected_transactions
    mock_read_excel.assert_called_once_with("data/transactions_excel.xlsx")
    dataframe.to_dict.assert_called_once_with(orient="records")
