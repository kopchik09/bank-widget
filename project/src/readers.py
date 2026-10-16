"""Чтение банковских транзакций из табличных файлов."""

from pathlib import Path
from typing import Any, TypeAlias, cast

import pandas as pd

FilePath: TypeAlias = str | Path
Transaction: TypeAlias = dict[str, Any]


def read_csv(file_path: FilePath) -> list[Transaction]:
    """Прочитать транзакции из CSV-файла с разделителем ``;``.

    Args:
        file_path: Путь к CSV-файлу с банковскими транзакциями.

    Returns:
        Список словарей: один словарь для каждой строки исходного файла.
    """
    dataframe = pd.read_csv(file_path, delimiter=";")
    return cast(list[Transaction], dataframe.to_dict(orient="records"))


def read_excel(file_path: FilePath) -> list[Transaction]:
    """Прочитать транзакции из Excel-файла формата XLSX.

    Args:
        file_path: Путь к Excel-файлу с банковскими транзакциями.

    Returns:
        Список словарей: один словарь для каждой строки исходного файла.
    """
    dataframe = pd.read_excel(file_path)
    return cast(list[Transaction], dataframe.to_dict(orient="records"))
