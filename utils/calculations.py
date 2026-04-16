def calculate_profit(direction, entry, exit, amount):
    if direction in ["buy", "long"]:
        return (exit - entry) * amount
    elif direction in ["sell", "short"]:
        return (entry - exit) * amount
    return 0


def calculate_total_capital(deals):
    return sum(d.profit for d in deals)


def equity_curve(deals):
    deals = sorted(deals, key=lambda d: d.date)

    balance = 0
    history = []

    for d in deals:
        balance += d.profit
        history.append({
            "date": d.date.strftime("%Y-%m-%d"),
            "balance": balance
        })

    return history