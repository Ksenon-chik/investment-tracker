from sqlalchemy.orm import Session
from models.deal import Deal
from services.deal import get_user_deals

def calculate_portfolio(db: Session, user_id: int):
    deals = get_user_deals(db, user_id)

    portfolio = {}

    for deal in deals:
        asset = deal.asset
        amount = deal.amount

        if deal.deal_type == "buy":
            portfolio[asset] = portfolio.get(asset, 0) + amount
        elif deal.deal_type == "sell":
            portfolio[asset] = portfolio.get(asset, 0) - amount

    return portfolio

def calculate_profit(db: Session, user_id: int):
    deals = get_user_deals(db, user_id)

    total_buy = 0
    total_sell = 0

    for deal in deals:
        value = deal.amount * deal.price

        if deal.deal_type == "buy":
            total_buy += value
        elif deal.deal_type == "sell":
            total_sell += value

    profit = total_sell - total_buy

    return {
        "total_buy": total_buy,
        "total_sell": total_sell,
        "profit": profit
    }

def calculate_profit(db: Session, user_id: int):
    deals = get_user_deals(db, user_id)

    total_buy = 0
    total_sell = 0

    for deal in deals:
        value = deal.amount * deal.price

        if deal.deal_type == "buy":
            total_buy += value
        elif deal.deal_type == "sell":
            total_sell += value

    profit = total_sell - total_buy

    return {
        "total_buy": total_buy,
        "total_sell": total_sell,
        "profit": profit
    }