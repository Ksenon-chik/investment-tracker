from sqlalchemy.orm import Session
from models.deal import Deal
from services.deal_service import get_user_deals

def calculate_portfolio(db: Session, user_id: int):
    deals = get_user_deals(db, user_id)

    portfolio = {}

    for deal in deals:
        asset = deal.asset
        amount = deal.amount

        if deal.direction == "buy":
            portfolio[asset] = portfolio.get(asset, 0) + amount
        elif deal.direction == "sell":
            portfolio[asset] = portfolio.get(asset, 0) - amount

    return portfolio

def calculate_profit(db: Session, user_id: int):
    deals = get_user_deals(db, user_id)

    total_buy = 0
    total_sell = 0

    for deal in deals:
        value = deal.amount * deal.price

        if deal.direction == "buy":
            total_buy += value
        elif deal.direction == "sell":
            total_sell += value

    profit = total_sell - total_buy

    return {
        "total_buy": total_buy,
        "total_sell": total_sell,
        "profit": profit
    }

def get_user_summary(db: Session, user_id: int):
    portfolio = calculate_portfolio(db, user_id)
    profit_data = calculate_profit(db, user_id)

    return {
        "portfolio": portfolio,
        "total_invested": profit_data["total_buy"],
        "total_returned": profit_data["total_sell"],
        "profit": profit_data["profit"]
    }

def get_full_analytics(db: Session, user_id: int):
    deals = get_user_deals(db, user_id)

    total_trades = len(deals)
    total_profit = 0
    total_loss = 0
    profitable_trades = 0

    profit_history = []
    cumulative_profit = 0

    for deal in deals:
        # подсчет прибыль/убыток
        if deal.result == "profit":
            total_profit += deal.amount
            profitable_trades += 1
            cumulative_profit += deal.amount

        elif deal.result == "loss":
            total_loss += deal.amount
            cumulative_profit -= deal.amount

        profit_history.append({
            "date": str(deal.date),
            "profit": cumulative_profit
        })

    winrate = (profitable_trades / total_trades * 100) if total_trades > 0 else 0

    return {
        "total_trades": total_trades,
        "total_profit": total_profit,
        "total_loss": total_loss,
        "winrate": round(winrate, 2),
        "profit_history": profit_history
    }