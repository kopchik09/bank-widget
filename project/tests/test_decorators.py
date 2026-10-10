import pytest

from project.src.decorators import log


# ---------- Вывод в консоль (capsys) ----------

def test_log_console_success(capsys):
    @log()
    def add(x, y):
        return x + y

    result = add(1, 2)

    assert result == 3
    captured = capsys.readouterr()
    assert captured.out == "add ok\n"


def test_log_console_error(capsys):
    @log()
    def divide(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    captured = capsys.readouterr()
    assert captured.out == "divide error: ZeroDivisionError. Inputs: (1, 0), {}\n"


def test_log_console_error_with_kwargs(capsys):
    @log()
    def divide(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(x=1, y=0)

    captured = capsys.readouterr()
    assert captured.out == "divide error: ZeroDivisionError. Inputs: (), {'x': 1, 'y': 0}\n"


# ---------- Запись в файл (tmp_path) ----------

def test_log_file_success(tmp_path):
    log_file = tmp_path / "mylog.txt"

    @log(filename=str(log_file))
    def add(x, y):
        return x + y

    result = add(1, 2)

    assert result == 3
    assert log_file.read_text(encoding="utf-8") == "add ok\n"


def test_log_file_error(tmp_path):
    log_file = tmp_path / "mylog.txt"

    @log(filename=str(log_file))
    def add(x, y):
        return x + y

    with pytest.raises(TypeError):
        add(1, "a")

    assert log_file.read_text(encoding="utf-8") == "add error: TypeError. Inputs: (1, 'a'), {}\n"


def test_log_file_appends(tmp_path):
    log_file = tmp_path / "mylog.txt"

    @log(filename=str(log_file))
    def add(x, y):
        return x + y

    add(1, 2)
    add(3, 4)

    assert log_file.read_text(encoding="utf-8") == "add ok\nadd ok\n"


def test_log_file_does_not_print_to_console(tmp_path, capsys):
    log_file = tmp_path / "mylog.txt"

    @log(filename=str(log_file))
    def add(x, y):
        return x + y

    add(1, 2)

    assert capsys.readouterr().out == ""


# ---------- Прочее поведение ----------

def test_log_preserves_function_name():
    @log()
    def my_function():
        """Документация"""

    assert my_function.__name__ == "my_function"
    assert my_function.__doc__ == "Документация"


def test_log_returns_result(capsys):
    @log()
    def get_text():
        return "привет"

    assert get_text() == "привет"
