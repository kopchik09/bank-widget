def get_mask_card_number(clean_number):
    if len(clean_number) == 16:
        masked_number = (
            f"{clean_number[:6]}{'*' * (len(clean_number) - 10)}{clean_number[-4:]}"
        )
        return " ".join(
            masked_number[i : i + 4] for i in range(0, len(masked_number), 4)
        )
    else:
        return f"Напишите номер счета правильно/n {get_mask_card_number(input())}"


def get_mask_account(clean_number):
    if len(clean_number) == 16:

        return f"**{clean_number[-4:]}"
    else:
        return f"Напишите номер счета правильно/n {get_mask_account(input())}"


# print(get_mask_account(input()))
# print(get_mask_card_number(input()))
