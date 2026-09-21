from masks import get_mask_account, get_mask_card_number

def mask_account_card(card):
    if card[0:4] == "Счет":
        return f"{card.split()[0]} **{card[-4:]}"
    else:
        return f"{" ".join(card.split()[:-1])} {get_mask_card_number(card.split()[-1])}"

#card = "MasterCard 7158300734726758"
#card = "Счет 35383033474447895560"
print(mask_account_card(input()))
