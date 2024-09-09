from loader import db

Currencies = {"UAH": 29.57, "RUB": 62.0, "EUR": 0.9}

def conveyor(user_id: int, element: list, summ: float) -> float:
    received = element[2]
    if received == '₽':
        received = 'RUB'
    elif received == '₴':
        received = 'UAH'
    elif received == '€':
        received = 'EUR'

    current = db.get_currency(user_id)
    if current == '₽':
        current = 'RUB'
    elif current == '₴':
        current = 'UAH'
    elif current == '€':
        current = 'EUR'
    else:
        current = received

    heft = summ / Currencies[current]
    db.set_currency(element[1], element[2])
    return db.set_balance(element[1], round(heft * Currencies[received], 2))


def conveyor2(summ: float, current: str, received: str) -> float:
    heft = summ / Currencies[current]
    return round(heft * Currencies[received], 2)
