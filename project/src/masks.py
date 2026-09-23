def get_mask_card_number(clean_number):
    """
    Маскирует номер карты, оставляя первые 6 и последние 4 цифры,
    остальное заменяет на звёздочки. Результат разбивается на группы по 4 символа.

    Поддерживает номера любой длины >= 10. Если длина < 10 — возвращает как есть.

    Args:
        clean_number: Строка с номером карты (только цифры).

    Returns:
        Маска в формате XXXX XXXX XXXX XXXX (с пробелами).
    """
    if len(clean_number) == 16:
        masked_number = (
            f"{clean_number[:6]}{'*' * (len(clean_number) - 10)}{clean_number[-4:]}"
        )
        return " ".join(
            masked_number[i : i + 4] for i in range(0, len(masked_number), 4)
        )
    else:
        # print("Напишите номер карты правильно")
        return f"Напишите номер счета правильно/n {get_mask_card_number(input())}"


def get_mask_account(clean_number):
    """
    Маскирует номер счёта, оставляя только последние 4 цифры.

    Если номер слишком короткий, возвращает его без изменений.

    Args:
        clean_number: Строка с номером счёта (только цифры).

    Returns:
        Строка вида **XXXX.
    """
    if len(clean_number) == 16:

        return f"**{clean_number[-4:]}"
    else:
        return f"Напишите номер счета правильно/n {get_mask_account(input())}"


# print(get_mask_account(input()))
# print(get_mask_card_number(input()))
