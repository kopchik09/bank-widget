import json
from pathlib import Path

from src.utils import load_transactions


def test_load_transactions_valid(tmp_path: Path) -> None:
    file = tmp_path / "ops.json"
    file.write_text(json.dumps([{"id": 1}, {"id": 2}]), encoding="utf-8")

    assert load_transactions(str(file)) == [{"id": 1}, {"id": 2}]


def test_load_transactions_empty_file(tmp_path: Path) -> None:
    file = tmp_path / "ops.json"
    file.write_text("", encoding="utf-8")

    assert load_transactions(str(file)) == []


def test_load_transactions_not_a_list(tmp_path: Path) -> None:
    file = tmp_path / "ops.json"
    file.write_text(json.dumps({"id": 1}), encoding="utf-8")

    assert load_transactions(str(file)) == []


def test_load_transactions_file_not_found(tmp_path: Path) -> None:
    assert load_transactions(str(tmp_path / "no_such_file.json")) == []
