from masks import get_mask_account, get_mask_card_number


def mask_account_card(card):
    """
    Маскирует строку с картой или счётом.

    Поддерживает два формата:
      - "Счет <номер>" — маскируется только конец номера счёта.
      - "<Тип карты> <номер>" — номер карты маскируется через get_mask_card_number.

    Args:
        card: Строка, содержащая тип и номер (например, "MasterCard 1234..." или "Счет 123...").

    Returns:
        Строка с замаскированным номером.
    """
    if card[0:4] == "Счет":
        return f"{card.split()[0]} **{card[-4:]}"
    else:
        return f"{' '.join(card.split()[:-1])} {get_mask_card_number(card.split()[-1])}"


def get_date(date):
    """
    Преобразует дату из формата ISO (YYYY-MM-DDTHH:MM:SS...) в DD.MM.YYYY.

    Работает только для строк, строго соответствующих формату YYYY-MM-DD...

    Args:
        date_iso: Дата в формате ISO (например, '2024-03-11T02:26:18.671407').

    Returns:
        Дата в формате DD.MM.YYYY (например, '11.03.2024').
    """
    return f"{date[8:10]}.{date[5:7]}.{date[:4]}"


if __name__ == "__main__":
    print(mask_account_card(input()))
    print(get_date(input()))
