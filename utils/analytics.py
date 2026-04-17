from collections import defaultdict


def calculate_stats(deals):
    total = len(deals)

    profit = 0
    loss = 0
    win_count = 0
    valid_trades = 0

    for d in deals:
        entry = getattr(d, "entry_price", None)
        exit_ = getattr(d, "exit_price", None)
        direction = getattr(d, "direction", None)
        amount = getattr(d, "amount", 0) or 0

        if entry is None or exit_ is None or direction is None:
            continue

        valid_trades += 1

        if direction in ["buy", "long"]:
            pnl = (exit_ - entry) * amount
        else:
            pnl = (entry - exit_) * amount

        if pnl >= 0:
            profit += pnl
            win_count += 1
        else:
            loss += pnl

    winrate = (win_count / valid_trades * 100) if valid_trades > 0 else 0

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
        if not getattr(d, "date", None):
            continue
        day = d.date.strftime("%a")
        if day in result:
            result[day] += 1

    return result


def asset_distribution(deals):
    result = defaultdict(int)

    for d in deals:
        asset = getattr(d, "asset", "Unknown")
        result[asset] += 1

    return dict(result)


def equity_curve(deals):
    balance = 0
    chart = []

    sorted_deals = sorted(
        [d for d in deals if getattr(d, "date", None)],
        key=lambda x: x.date
    )

    for d in sorted_deals:
        entry = getattr(d, "entry_price", None)
        exit_ = getattr(d, "exit_price", None)
        direction = getattr(d, "direction", None)
        amount = getattr(d, "amount", 0) or 0

        if entry is None or exit_ is None or direction is None:
            continue

        if direction in ["buy", "long"]:
            pnl = (exit_ - entry) * amount
        else:
            pnl = (entry - exit_) * amount

        balance += pnl

        chart.append({
            "date": d.date.strftime("%Y-%m-%d"),
            "balance": round(balance, 2)
        })

    return chart