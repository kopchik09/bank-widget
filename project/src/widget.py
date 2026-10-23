from src.masks import get_mask_card_number


def mask_account_card(card: str) -> str:
    """Маскирует строку вида "Visa Platinum 7000792289606361" или "Счет 35383033474447895560"."""
    if card.startswith("Счет"):
        return f"Счет **{card[-4:]}"

    parts = card.split()
    name, number = " ".join(parts[:-1]), parts[-1]
    try:
        return f"{name} {get_mask_card_number(number)}"
    except ValueError:
        return card


def get_date(date: str) -> str:
    """Переводит дату из "2024-03-11T02:26:18.671407" в "11.03.2024"."""
    return f"{date[8:10]}.{date[5:7]}.{date[:4]}"
