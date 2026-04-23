from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from services.deal_service import get_user_deals
from sqlalchemy.orm import Session
from db.session import get_db
from utils.dependencies import get_current_user
from datetime import datetime
from utils.analytics import equity_curve

router = APIRouter(prefix="/profile", tags=["Profile"])

templates = Jinja2Templates(directory="templates")

@router.get("/")
def profile_page(request: Request, db: Session = Depends(get_db)):
    # 1. Берем ID из куки, как это делал main.py
    user_id = request.cookies.get("user_id")
    
    if not user_id:
        from fastapi.responses import RedirectResponse
        return RedirectResponse("/auth-page")

    # 2. Получаем объект пользователя
    from services.user_service import get_user_by_id
    user = get_user_by_id(db, int(user_id))
    
    if not user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse("/auth-page")

    # 3. Дальше твой код графика БЕЗ ИЗМЕНЕНИЙ
    deals = user.deals # или get_user_deals(db, user.id)
    
    start_balance = float(user.start_balance or 100.0)
    current_cumulative = start_balance
    
    final_chart_data = []
    final_chart_data.append({"date": "Старт", "balance": round(current_cumulative, 2)})

    # Сортируем сделки
    sorted_deals = sorted(deals, key=lambda x: x.date if x.date else datetime.now())
    
    for d in sorted_deals:
        pnl = float(d.profit or 0)
        current_cumulative += pnl
        final_chart_data.append({
            "date": d.date.strftime("%d.%m") if d.date else "??",
            "balance": round(current_cumulative, 2)
        })

    if len(final_chart_data) == 1:
        final_chart_data.append({"date": "Сегодня", "balance": round(current_cumulative, 2)})

    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": user,
        "total_capital": round(current_cumulative, 2),
        "chart_data": final_chart_data
    })