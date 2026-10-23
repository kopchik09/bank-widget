"""Отчёты по банковским транзакциям."""
import json
import logging
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional, TypeVar, overload

import pandas as pd

logger = logging.getLogger(__name__)
F = TypeVar("F", bound=Callable[..., Any])


def save_report(func: Optional[F] = None, *, filename: str = "report.json"):
    """
    Декоратор сохраняет результат отчёта в JSON-файл.

    Использование: @save_report или @save_report(filename="my_report.json").
    DataFrame сохраняется как JSON records, остальные результаты — как JSON.
    """
    def decorator(report_func: F) -> F:
        @wraps(report_func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = report_func(*args, **kwargs)
            path = Path(filename)
            try:
                if isinstance(result, pd.DataFrame):
                    payload = result.to_json(orient="records", force_ascii=False, date_format="iso")
                else:
                    payload = json.dumps(result, ensure_ascii=False, default=str, indent=2)
                path.write_text(payload + "\n", encoding="utf-8")
                logger.info("Отчёт %s сохранён в %s", report_func.__name__, path)
            except OSError:
                logger.exception("Не удалось сохранить отчёт в %s", path)
                raise
            return result
        return wrapper  # type: ignore[return-value]

    if func is not None:
        return decorator(func)
    return decorator


def _column(data: pd.DataFrame, candidates: tuple[str, ...]) -> str | None:
    return next((name for name in candidates if name in data.columns), None)


@save_report
def spending_by_category(
    transactions: pd.DataFrame,
    category: str,
    date: Optional[str] = None,
) -> pd.DataFrame:
    """
    Возвращает строки выбранной категории за три месяца до указанной даты включительно.

    Поддерживаются названия столбцов из русскоязычного Excel и английские варианты.
    """
    date_column = _column(transactions, ("Дата операции", "date", "Дата"))
    category_column = _column(transactions, ("Категория", "category"))
    if date_column is None or category_column is None:
        logger.warning("В таблице отсутствует столбец даты или категории")
        return transactions.iloc[0:0].copy()

    reference_date = pd.Timestamp(date) if date else pd.Timestamp(datetime.now().date())
    dates = pd.to_datetime(transactions[date_column], errors="coerce", format="mixed", dayfirst=True)
    start_date = reference_date - pd.DateOffset(months=3)
    mask = (
        dates.ge(start_date)
        & dates.le(reference_date + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1))
        & transactions[category_column].astype(str).str.casefold().eq(category.casefold())
    )
    return transactions.loc[mask].copy()
