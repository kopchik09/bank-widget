import logging
from pathlib import Path

LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOGS_DIR / "masks.log", mode="w", encoding="utf-8")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)


def get_mask_card_number(clean_number: str) -> str:
    """Маскирует номер карты: 7000 79** **** 6361."""
    logger.info("Маскировка номера карты")

    if len(clean_number) != 16 or not clean_number.isdigit():
        logger.error("Некорректный номер карты: длина %d", len(clean_number))
        raise ValueError("Номер карты должен состоять из 16 цифр")

    masked_number = f"{clean_number[:6]}{'*' * 6}{clean_number[-4:]}"
    result = " ".join(masked_number[i : i + 4] for i in range(0, 16, 4))

    logger.info("Номер карты успешно замаскирован")
    return result


def get_mask_account(clean_number: str) -> str:
    """Маскирует номер счёта: **4305."""
    logger.info("Маскировка номера счёта")

    if len(clean_number) < 4 or not clean_number.isdigit():
        logger.error("Некорректный номер счёта: длина %d", len(clean_number))
        raise ValueError("Номер счёта должен содержать минимум 4 цифры")

    logger.info("Номер счёта успешно замаскирован")
    return f"**{clean_number[-4:]}"
