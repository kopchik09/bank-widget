from masks import get_mask_account, get_mask_card_number

def mask_account_card(card):
    if card[0:4] == "Счет":
        return f"{card.split()[0]} **{card[-4:]}"
    else:
        return f"{" ".join(card.split()[:-1])} {get_mask_card_number(card.split()[-1])}"
def get_date(date):
    return f"{date[8:10]}.{date[5:7]}.{date[:4]}"
#card = "MasterCard 7158300734726758"
#card = "Счет 35383033474447895560"
print(mask_account_card(input()))
#date = "2024-03-11T02:26:18.671407"
print(get_date(input()))