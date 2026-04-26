from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime

from db.session import get_db
from utils.dependencies import get_current_user

router = APIRouter(prefix="/profile", tags=["Profile"])

templates = Jinja2Templates(directory="templates")


@router.get("/")
def profile_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # проверка авторизован ли пользователь
    if not current_user:
        return RedirectResponse("/auth-page")

    user = current_user

    # сделки пользователя
    deals = user.deals

    # стартовый баланс
    start_balance = float(user.start_balance or 0)
    current_cumulative = start_balance

    # график
    final_chart_data = []
    final_chart_data.append({
        "date": "Старт",
        "balance": round(current_cumulative, 2)
    })

    # сортировка сделок
    sorted_deals = sorted(
        deals,
        key=lambda x: x.date if x.date else datetime.now()
    )

    # подсчет капитала
    for d in sorted_deals:
        pnl = float(d.profit or 0)
        current_cumulative += pnl

        final_chart_data.append({
            "date": d.date.strftime("%d.%m") if d.date else "??",
            "balance": round(current_cumulative, 2)
        })

    # если нет сделок
    if len(final_chart_data) == 1:
        final_chart_data.append({
            "date": "Сегодня",
            "balance": round(current_cumulative, 2)
        })

    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": user,
        "total_capital": round(current_cumulative, 2),
        "chart_data": final_chart_data
    })