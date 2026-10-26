"""Формирование отчетов по банковским операциям.

Основной отчет — расходы по категориям.

Ожидается, что операции представлены словарями с полями:
    amount (или сумма) — сумма операции;
    category (или категория) — категория операции;
    описание/description — необязательное описание;
    date/дата — необязательная дата.

По умолчанию расходами считаются операции с отрицательной суммой.
Если в данных суммы расходов положительные, передайте ``expenses_only=False``
или укажите собственный ``is_expense``.
"""

from collections import defaultdict
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Callable, Iterable


def _first_value(operation: dict[str, Any], *keys: str, default: Any = None) -> Any:
    """Возвращает первое непустое значение из перечисленных ключей."""
    for key in keys:
        value = operation.get(key)
        if value is not None and value != "":
            return value
    return default


def _to_decimal(value: Any) -> Decimal:
    """Преобразует сумму в Decimal, поддерживая строки с запятой."""
    if isinstance(value, Decimal):
        return value
    if value is None:
        return Decimal("0")
    normalized = str(value).strip().replace(" ", "").replace(",", ".")
    # Часто суммы в выгрузках содержат символ валюты.
    for symbol in ("₽", "$", "€", "руб.", "руб"):
        normalized = normalized.replace(symbol, "")
    try:
        return Decimal(normalized)
    except InvalidOperation as exc:
        raise ValueError(f"Некорректная сумма операции: {value!r}") from exc


def _to_date(value: Any) -> date | None:
    """Разбирает распространенные форматы даты."""
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    text = str(value).strip()
    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(text[:19], fmt).date()
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date()
    except ValueError:
        return None


def expenses_by_category(
    operations: Iterable[dict[str, Any]],
    *,
    start_date: date | str | None = None,
    end_date: date | str | None = None,
    expenses_only: bool = True,
    is_expense: Callable[[dict[str, Any]], bool] | None = None,
) -> list[dict[str, Any]]:
    """Возвращает расходы, сгруппированные по категориям.

    Args:
        operations: последовательность операций-словарей.
        start_date: включительная нижняя граница даты (date или YYYY-MM-DD).
        end_date: включительная верхняя граница даты (date или YYYY-MM-DD).
        expenses_only: если True, учитывать только отрицательные суммы.
        is_expense: необязательная функция определения расхода. Если задана,
            она имеет приоритет над ``expenses_only``.

    Returns:
        Список словарей, отсортированный по убыванию расходов:
        ``{"category": "Еда", "total": Decimal("1250.00"), "count": 3}``.
        Значение total всегда положительное.
    """
    def parse_bound(value: date | str | None) -> date | None:
        if value is None or isinstance(value, date):
            return value
        parsed = _to_date(value)
        if parsed is None:
            raise ValueError(f"Не удалось разобрать дату: {value!r}")
        return parsed

    start = parse_bound(start_date)
    end = parse_bound(end_date)
    if start and end and start > end:
        raise ValueError("start_date не может быть позже end_date")

    totals: dict[str, Decimal] = defaultdict(Decimal)
    counts: dict[str, int] = defaultdict(int)

    for operation in operations:
        raw_amount = _first_value(operation, "amount", "сумма", "sum", "Сумма", default=0)
        amount = _to_decimal(raw_amount)

        if is_expense is not None:
            expense = is_expense(operation)
        else:
            expense = amount < 0 if expenses_only else True
        if not expense:
            continue

        raw_date = _first_value(operation, "date", "дата", "operation_date", "Дата")
        operation_date = _to_date(raw_date)
        if start or end:
            # При заданном периоде операции без даты не включаются.
            if operation_date is None:
                continue
            if start and operation_date < start:
                continue
            if end and operation_date > end:
                continue

        category = str(
            _first_value(operation, "category", "категория", "Категория", default="Без категории")
        ).strip() or "Без категории"

        totals[category] += abs(amount)
        counts[category] += 1

    result = [
        {"category": category, "total": total, "count": counts[category]}
        for category, total in totals.items()
    ]
    return sorted(result, key=lambda item: (-item["total"], item["category"].casefold()))


def format_expenses_by_category(
    operations: Iterable[dict[str, Any]],
    *,
    currency: str = "₽",
    start_date: date | str | None = None,
    end_date: date | str | None = None,
    expenses_only: bool = True,
) -> str:
    """Формирует человекочитаемый текстовый отчет."""
    rows = expenses_by_category(
        operations,
        start_date=start_date,
        end_date=end_date,
        expenses_only=expenses_only,
    )
    if not rows:
        return "За выбранный период расходов не найдено."

    total = sum((row["total"] for row in rows), Decimal("0"))
    lines = ["Расходы по категориям:"]
    for row in rows:
        lines.append(
            f'- {row["category"]}: {row["total"]:.2f} {currency} '
            f'({row["count"]} операций)'
        )
    lines.append(f"Итого: {total:.2f} {currency}")
    return "\n".join(lines)
