from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from fastapi.templating import Jinja2Templates
from services.deal_service import get_user_deals

router = APIRouter(prefix="/analytics", tags=["Analytics"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
def analytics_page(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")

    if not user_id:
        return templates.TemplateResponse("auth.html", {"request": request})

    deals = get_user_deals(db, int(user_id))

    # БАЗОВАЯ СТАТИСТИКА
    total_deals = len(deals)

    total_profit = 0
    total_loss = 0
    win_trades = 0

    for d in deals:
        if d.price_close is None:
            continue

        if d.direction in ["buy", "long"]:
            profit = (d.price_close - d.price_open) * d.amount
        else:  # sell / short
            profit = (d.price_open - d.price_close) * d.amount

        if profit > 0:
            total_profit = sum(
                d.amount * d.price
                for d in deals
                if d.type == "sell")
            win_trades += 1
        else:
            total_loss += abs(profit)

    winrate = 0
    if total_deals > 0:
        winrate = round(
            len([d for d in deals if d.result == "profit"]) / total_deals * 100, 2
        )

    # ГРАФИК КАПИТАЛА
    chart_data = []
    balance = 0

    for d in sorted(deals, key=lambda x: x.date):
        pnl = d.amount * d.price
        if d.result == "loss":
            pnl *= -1

        balance += pnl

        chart_data.append({
            "date": d.date.strftime("%Y-%m-%d"),
            "balance": balance
        })

    # АКТИВЫ
    assets_data = {}

    for d in deals:
        assets_data[d.asset] = assets_data.get(d.asset, 0) + 1

    # СДЕЛКИ ПО ДНЯМ
    week_data = {
        "Mon": 0, "Tue": 0, "Wed": 0,
        "Thu": 0, "Fri": 0, "Sat": 0, "Sun": 0
    }

    for d in deals:
        day = d.date.strftime("%a")
        if day in week_data:
            week_data[day] += 1

    # Передача всех пунктов!
    return templates.TemplateResponse("analytics.html", {
        "request": request,
        "total_deals": total_deals,
        "total_profit": total_profit,
        "total_loss": total_loss,
        "winrate": winrate,
        "chart_data": chart_data,
        "assets_data": assets_data,
        "week_data": week_data
    })