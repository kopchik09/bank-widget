from typing import Any, Callable

from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.readers import read_csv, read_xlsx
from src.search import process_bank_search
from src.utils import load_transactions
from src.widget import get_date, mask_account_card

STATUSES = ("EXECUTED", "CANCELED", "PENDING")

# пункт меню -> (название формата, путь к файлу, функция чтения)
SOURCES: dict[str, tuple[str, str, Callable[[str], list[dict[str, Any]]]]] = {
    "1": ("JSON", "data/operations.json", load_transactions),
    "2": ("CSV", "data/transactions.csv", read_csv),
    "3": ("XLSX", "data/transactions_excel.xlsx", read_xlsx),
}


def ask_yes_no(question: str) -> bool:
    """Задаёт вопрос, пока пользователь не ответит «да» или «нет»."""
    while True:
        answer = input(f"{question} Да/Нет\n").strip().lower()
        if answer == "да":
            return True
        if answer == "нет":
            return False
        print('Пожалуйста, ответьте "Да" или "Нет".')


def ask_status() -> str:
    """Спрашивает статус, пока не будет введён допустимый. Регистр не важен."""
    while True:
        print(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            f"Доступные для фильтровки статусы: {', '.join(STATUSES)}"
        )
        status = input().strip()
        if status.upper() in STATUSES:
            print(f'Операции отфильтрованы по статусу "{status.upper()}"')
            return status.upper()
        print(f'Статус операции "{status}" недоступен.\n')


def ask_sort_descending() -> bool:
    """Спрашивает направление сортировки. True — по убыванию."""
    while True:
        answer = input("Отсортировать по возрастанию или по убыванию?\n").strip().lower()
        if answer == "по возрастанию":
            return False
        if answer == "по убыванию":
            return True
        print('Напишите "по возрастанию" или "по убыванию".')


def format_amount(operation: dict[str, Any]) -> str:
    """Возвращает сумму операции вместе с валютой: "8200 EUR" или "40542 руб."."""
    amount_info = operation.get("operationAmount", {})
    code = amount_info.get("currency", {}).get("code", "")
    raw_amount = str(amount_info.get("amount", ""))
    try:
        value = float(raw_amount)
        amount = str(int(value)) if value.is_integer() else f"{value:.2f}"
    except ValueError:
        amount = raw_amount
    currency = "руб." if code == "RUB" else code
    return f"{amount} {currency}".strip()


def format_operation(operation: dict[str, Any]) -> str:
    """Собирает текст одной операции для вывода в консоль."""
    date = get_date(str(operation.get("date", "")))
    description = operation.get("description", "")

    source = operation.get("from")
    target = operation.get("to")
    if source and target:
        route = f"{mask_account_card(str(source))} -> {mask_account_card(str(target))}"
    else:
        route = mask_account_card(str(source or target or ""))

    return f"{date} {description}\n{route}\nСумма: {format_amount(operation)}\n"


def main() -> None:
    print(
        "Привет! Добро пожаловать в программу работы с банковскими транзакциями.\n"
        "Выберите необходимый пункт меню:\n"
        "1. Получить информацию о транзакциях из JSON-файла\n"
        "2. Получить информацию о транзакциях из CSV-файла\n"
        "3. Получить информацию о транзакциях из XLSX-файла"
    )

    choice = input().strip()
    while choice not in SOURCES:
        print("Выберите пункт меню: 1, 2 или 3.")
        choice = input().strip()

    name, path, reader = SOURCES[choice]
    print(f"Для обработки выбран {name}-файл.")

    transactions = reader(path)
    transactions = filter_by_state(transactions, ask_status())

    if ask_yes_no("Отсортировать операции по дате?"):
        transactions = sort_by_date(transactions, ask_sort_descending())

    if ask_yes_no("Выводить только рублевые транзакции?"):
        transactions = list(filter_by_currency(transactions, "RUB"))

    if ask_yes_no("Отфильтровать список транзакций по определенному слову в описании?"):
        word = input("Введите слово для поиска:\n").strip()
        transactions = process_bank_search(transactions, word)

    print("Распечатываю итоговый список транзакций...\n")

    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(transactions)}\n")
    for operation in transactions:
        print(format_operation(operation))


if __name__ == "__main__":
    main()
