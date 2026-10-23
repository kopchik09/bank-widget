from typing import Any

import pytest

import main as main_module
from main import ask_status, ask_yes_no, format_amount, format_operation

TRANSACTIONS: list[dict[str, Any]] = [
    {
        "id": 1,
        "state": "EXECUTED",
        "date": "2019-12-08T22:46:21.935582",
        "operationAmount": {"amount": "40542.00", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Открытие вклада",
        "to": "Счет 90424923579946435907",
    },
    {
        "id": 2,
        "state": "EXECUTED",
        "date": "2019-11-12T20:30:00",
        "operationAmount": {"amount": "130", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод с карты на карту",
        "from": "MasterCard 7771270000003727",
        "to": "Visa Platinum 1293380000009203",
    },
    {
        "id": 3,
        "state": "EXECUTED",
        "date": "2018-07-18T10:00:00",
        "operationAmount": {"amount": "8390", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Visa Platinum 7492650000007202",
        "to": "Счет 12340000000000000034",
    },
    {
        "id": 4,
        "state": "CANCELED",
        "date": "2018-06-03T10:00:00",
        "operationAmount": {"amount": "8200", "currency": {"name": "EUR", "code": "EUR"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 11110000000000002935",
        "to": "Счет 22220000000000004321",
    },
]


def feed_input(monkeypatch: pytest.MonkeyPatch, answers: list[str]) -> None:
    """Подставляет заранее заготовленные ответы вместо input()."""
    iterator = iter(answers)
    monkeypatch.setattr("builtins.input", lambda *args: next(iterator))


def use_fake_sources(monkeypatch: pytest.MonkeyPatch, data: list[dict[str, Any]]) -> None:
    """Подменяет чтение файлов, чтобы тесты не зависели от data/."""
    for key, (name, path, _) in list(main_module.SOURCES.items()):
        monkeypatch.setitem(main_module.SOURCES, key, (name, path, lambda _path: data))


def run_main(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    answers: list[str],
    data: list[dict[str, Any]] = TRANSACTIONS,
) -> str:
    use_fake_sources(monkeypatch, data)
    feed_input(monkeypatch, answers)
    main_module.main()
    return capsys.readouterr().out


# ---------- ask_yes_no ----------

def test_ask_yes_no_yes(monkeypatch: pytest.MonkeyPatch) -> None:
    feed_input(monkeypatch, ["ДА"])

    assert ask_yes_no("Вопрос?") is True


def test_ask_yes_no_no(monkeypatch: pytest.MonkeyPatch) -> None:
    feed_input(monkeypatch, ["  нет "])

    assert ask_yes_no("Вопрос?") is False


def test_ask_yes_no_repeats_on_wrong_answer(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    feed_input(monkeypatch, ["может", "да"])

    assert ask_yes_no("Вопрос?") is True
    assert 'Пожалуйста, ответьте "Да" или "Нет".' in capsys.readouterr().out


# ---------- ask_status ----------

@pytest.mark.parametrize("answer", ["EXECUTED", "executed", "Executed"])
def test_ask_status_ignores_case(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], answer: str
) -> None:
    feed_input(monkeypatch, [answer])

    assert ask_status() == "EXECUTED"
    assert 'Операции отфильтрованы по статусу "EXECUTED"' in capsys.readouterr().out


def test_ask_status_repeats_on_unknown_status(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    feed_input(monkeypatch, ["test", "pending"])

    assert ask_status() == "PENDING"
    output = capsys.readouterr().out
    assert 'Статус операции "test" недоступен.' in output
    assert output.count("Введите статус") == 2


# ---------- форматирование ----------

@pytest.mark.parametrize(
    ("amount", "code", "expected"),
    [
        ("40542.00", "RUB", "40542 руб."),
        ("130", "USD", "130 USD"),
        ("8200.5", "EUR", "8200.50 EUR"),
        ("abc", "USD", "abc USD"),
    ],
)
def test_format_amount(amount: str, code: str, expected: str) -> None:
    operation = {"operationAmount": {"amount": amount, "currency": {"code": code}}}

    assert format_amount(operation) == expected


def test_format_operation_with_source_and_target() -> None:
    assert format_operation(TRANSACTIONS[1]) == (
        "12.11.2019 Перевод с карты на карту\n"
        "MasterCard 7771 27** **** 3727 -> Visa Platinum 1293 38** **** 9203\n"
        "Сумма: 130 USD\n"
    )


def test_format_operation_without_source() -> None:
    assert format_operation(TRANSACTIONS[0]) == (
        "08.12.2019 Открытие вклада\n"
        "Счет **5907\n"
        "Сумма: 40542 руб.\n"
    )


# ---------- main ----------

def test_main_full_scenario(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    output = run_main(
        monkeypatch, capsys,
        ["1", "executed", "да", "по возрастанию", "нет", "нет"],
    )

    assert "Для обработки выбран JSON-файл." in output
    assert "Всего банковских операций в выборке: 3" in output
    # по возрастанию: сначала 2018, потом 2019
    assert output.index("18.07.2018") < output.index("12.11.2019") < output.index("08.12.2019")


def test_main_sort_descending(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    output = run_main(
        monkeypatch, capsys,
        ["1", "EXECUTED", "да", "по убыванию", "нет", "нет"],
    )

    assert output.index("08.12.2019") < output.index("12.11.2019") < output.index("18.07.2018")


def test_main_without_sorting_keeps_file_order(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    output = run_main(monkeypatch, capsys, ["1", "EXECUTED", "нет", "нет", "нет"])

    assert output.index("08.12.2019") < output.index("12.11.2019") < output.index("18.07.2018")


def test_main_only_rub(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    output = run_main(monkeypatch, capsys, ["1", "EXECUTED", "нет", "да", "нет"])

    assert "Всего банковских операций в выборке: 2" in output
    assert "USD" not in output


def test_main_search_by_word(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    output = run_main(monkeypatch, capsys, ["1", "EXECUTED", "нет", "нет", "да", "ВКЛАД"])

    assert "Всего банковских операций в выборке: 1" in output
    assert "Открытие вклада" in output


def test_main_status_canceled(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    output = run_main(monkeypatch, capsys, ["1", "canceled", "нет", "нет", "нет"])

    assert "Всего банковских операций в выборке: 1" in output
    assert "Сумма: 8200 EUR" in output


def test_main_empty_result(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    output = run_main(monkeypatch, capsys, ["1", "pending", "нет", "нет", "нет"])

    assert "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации" in output
    assert "Всего банковских операций" not in output


def test_main_empty_file(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    output = run_main(monkeypatch, capsys, ["1", "executed", "нет", "нет", "нет"], data=[])

    assert "Не найдено ни одной транзакции" in output


def test_main_repeats_menu_on_wrong_choice(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    output = run_main(monkeypatch, capsys, ["9", "2", "executed", "нет", "нет", "нет"])

    assert "Выберите пункт меню: 1, 2 или 3." in output
    assert "Для обработки выбран CSV-файл." in output


@pytest.mark.parametrize(("choice", "name"), [("1", "JSON"), ("2", "CSV"), ("3", "XLSX")])
def test_main_menu_choices(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    choice: str,
    name: str,
) -> None:
    output = run_main(monkeypatch, capsys, [choice, "executed", "нет", "нет", "нет"])

    assert f"Для обработки выбран {name}-файл." in output
