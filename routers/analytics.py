from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from fastapi.templating import Jinja2Templates
from services.deal_service import get_user_deals

# импорт логики
from utils.analytics import (
    calculate_stats,
    deals_by_day,
    asset_distribution,
    equity_curve
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
def analytics_page(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")

    if not user_id:
        from fastapi.responses import RedirectResponse
        return RedirectResponse("/auth-page")

    # Получаем пользователя, чтобы узнать его баланс
    from services.user_service import get_user_by_id
    user = get_user_by_id(db, int(user_id))
    
    if not user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse("/auth-page")

    deals = user.deals  # Сделки пользователя

    # Расчеты
    stats = calculate_stats(deals)
    week_data = deals_by_day(deals)
    assets_data = asset_distribution(deals)
    
    chart_data = equity_curve(deals, user.start_balance)

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