from collections import defaultdict
from datetime import datetime


def calculate_stats(deals):
    total = len(deals)

    profit = 0
    loss = 0
    win_count = 0

    for d in deals:
        # прибыль/убыток
        if d.direction in ["buy", "long"]:
            pnl = (d.exit_price - d.entry_price) * d.amount
        else:
            pnl = (d.entry_price - d.exit_price) * d.amount

        if pnl >= 0:
            profit += pnl
            win_count += 1
        else:
            loss += pnl

    winrate = (win_count / total * 100) if total > 0 else 0

    return {
        "total": total,
        "profit": round(profit, 2),
        "loss": round(loss, 2),
        "winrate": round(winrate, 2)
    }


def deals_by_day(deals):
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    result = {day: 0 for day in days}

    for d in deals:
        day = d.date.strftime("%a")
        result[day] += 1

    return result


def asset_distribution(deals):
    result = defaultdict(int)

    for d in deals:
        result[d.asset] += 1

    return dict(result)