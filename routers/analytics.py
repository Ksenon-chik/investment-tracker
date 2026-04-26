from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from utils.dependencies import get_current_user

from utils.analytics import (
    calculate_stats,
    deals_by_day,
    asset_distribution,
    equity_curve
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
def analytics_page(
    request: Request, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) # Проверка JWT
):
    # редирект токена если невалидный
    if not current_user:
        return RedirectResponse("/auth-page")

    # сделки из объекта пользователя
    deals = current_user.deals 

    # Расчеты (start_balance текущего юзера)
    stats = calculate_stats(deals)
    week_data = deals_by_day(deals)
    assets_data = asset_distribution(deals)
    
    chart_data = equity_curve(deals, current_user.start_balance)

    return templates.TemplateResponse("analytics.html", {
        "request": request,
        "total_deals": stats["total"],
        "total_profit": stats["profit"],
        "total_loss": stats["loss"],
        "winrate": stats["winrate"],
        "chart_data": chart_data,
        "assets_data": assets_data,
        "week_data": week_data
    })