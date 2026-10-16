# Bank Widget

Набор функций для обработки банковских транзакций. Проект умеет работать с
операциями в форматах JSON, CSV и XLSX, маскировать реквизиты, фильтровать и
сортировать транзакции, а также конвертировать суммы в рубли через внешний API.

## Возможности

- Маскирование номеров банковских карт и счетов.
- Форматирование даты операции из ISO-формата в `ДД.ММ.ГГГГ`.
- Фильтрация транзакций по статусу и сортировка по дате.
- Генераторы для отбора операций по валюте, получения описаний и формирования
  номеров карт.
- Чтение транзакций из JSON, CSV и XLSX-файлов с возвратом `list[dict]`.
- Декоратор логирования результатов вызова функций.
- Конвертация операций в USD и EUR в рубли через API Exchange Rates Data.

## Структура

```text
project/
├── src/
│   ├── decorators.py    # декоратор логирования
│   ├── external_api.py  # конвертация валют через API
│   ├── generators.py    # функции-генераторы для транзакций
│   ├── masks.py         # маскирование счетов и карт
│   ├── processing.py    # фильтрация и сортировка операций
│   ├── readers.py       # чтение CSV и XLSX
│   ├── utils.py         # чтение JSON
│   └── widget.py        # пользовательские функции форматирования
└── tests/               # тесты Pytest
```

## Требования

- Python 3.13 или новее.
- Зависимости из `requirements.txt`.
- API-ключ Exchange Rates Data — только для конвертации USD и EUR в RUB.

## Установка

1. Откройте папку проекта в терминале.
2. Создайте виртуальное окружение:

   ```bash
   python -m venv .venv
   ```

3. Активируйте его:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

4. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

5. Если нужна конвертация валют, создайте файл `.env` рядом с
   `pyproject.toml` и добавьте ключ:

   ```env
   API_KEY=ваш_ключ_Exchange_Rates_Data
   ```

   В качестве шаблона можно использовать `.env.example`. Файл `.env` не нужно
   добавлять в репозиторий.

## Примеры использования

### Чтение JSON

```python
from project.src.utils import load_transactions

transactions = load_transactions("data/operations.json")
```

### Чтение CSV и Excel

CSV-файл должен использовать разделитель `;`.

```python
from project.src.readers import read_csv, read_excel

csv_transactions = read_csv("data/transactions.csv")
excel_transactions = read_excel("data/transactions_excel.xlsx")
```

Обе функции возвращают список словарей: один словарь на строку исходного
файла.

### Фильтрация и сортировка

```python
from project.src.processing import filter_by_state, sort_by_date

executed = filter_by_state(transactions, "EXECUTED")
newest_first = sort_by_date(executed)
```

### Маскирование реквизитов

```python
from project.src.masks import get_mask_account, get_mask_card_number

card = get_mask_card_number("7000792289606361")
account = get_mask_account("73654108430135874305")
```

### Конвертация валюты

```python
from project.src.external_api import get_transaction_amount_rub

transaction = {
    "operationAmount": {
        "amount": "100",
        "currency": {"code": "USD"},
    }
}

amount_rub = get_transaction_amount_rub(transaction)
```

Операции в RUB возвращаются без обращения к API. Для USD и EUR требуется
переменная окружения `API_KEY`.

## Проверка качества

```bash
pytest
flake8
isort --check-only .
black --check .
mypy project
```

## Лицензия

Проект распространяется для учебных целей.
