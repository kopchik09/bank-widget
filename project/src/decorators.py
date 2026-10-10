from functools import wraps
from typing import Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Логирует результат работы функции: в файл, если задан filename,
    иначе в консоль.
    """

    def write_log(message: str) -> None:
        if filename:
            with open(filename, "a", encoding="utf-8") as file:
                file.write(message + "\n")
        else:
            print(message)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                write_log(f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}")
                raise
            write_log(f"{func.__name__} ok")
            return result

        return wrapper

    return decorator


if __name__ == "__main__":
    @log()
    def my_function(x, y):
        return x + y

    my_function(1, 2)
    # в mylog.txt: my_function ok

    # @log()
    # def divide(x, y):
    #    return x / y
    #
    #
    # divide(1, 0)
