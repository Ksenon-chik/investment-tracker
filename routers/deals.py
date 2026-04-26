from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime

from db.session import get_db
from models.deal import Deal
from services.deal_service import get_user_deals
from utils.calculations import calculate_profit
from utils.dependencies import get_current_user

router = APIRouter(prefix="/deals", tags=["Deals"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def deals_page(
    request: Request, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) # JWT токен
):
    if not current_user:
        return RedirectResponse("/auth-page")

    # ID токена
    deals = get_user_deals(db, current_user.id)

    return templates.TemplateResponse("deals.html", {
        "request": request,
        "deals": deals
    })

@router.post("/create")
def create_deal(
    request: Request,
    asset: str = Form(""),
    direction: str = Form(""),
    amount: str = Form(""),
    entry_price: str = Form(""),
    exit_price: str = Form(""),
    date: str = Form(""),
    timeframe: str = Form(""),
    comment: str = Form(""),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) # текущий юзер
):
    if not current_user:
        return RedirectResponse("/auth-page", status_code=303)

    # проверка обязательных полей
    if not asset or not direction or not amount or not entry_price or not exit_price or not date:
        return RedirectResponse(
            "/deals?error=Заполни обязательные поля",
            status_code=303
        )

    # проверка значений
    try:
        amount = float(amount)
        entry_price = float(entry_price)
        exit_price = float(exit_price)
    except:
        return RedirectResponse(
            "/deals?error=Числа введены неверно",
            status_code=303
        )

    if amount <= 0:
        return RedirectResponse(
            "/deals?error=Объем должен быть больше 0",
            status_code=303
        )

    if entry_price <= 0 or exit_price <= 0:
        return RedirectResponse(
            "/deals?error=Цена должна быть больше 0",
            status_code=303
        )

    # проверка даты
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except:
        return RedirectResponse(
            "/deals?error=Неверная дата",
            status_code=303
        )

    # профит
    profit = calculate_profit(direction, entry_price, exit_price, amount)

    # создание
    deal = Deal(
        user_id=current_user.id,
        asset=asset.strip(),
        direction=direction,
        amount=amount,
        entry_price=entry_price,
        exit_price=exit_price,
        profit=profit,
        timeframe=timeframe.strip() if timeframe else None,  # опционально
        comment=comment.strip() if comment else None,        # опционально
        date=date_obj
    )

    db.add(deal)
    db.commit()

    return RedirectResponse("/deals", status_code=303)


@router.post("/delete-selected")
def delete_selected(
    request: Request,
    deal_id: int = Form(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not current_user: # проверка токена
        return RedirectResponse("/auth-page")

    if not deal_id:
        return RedirectResponse(
            "/deals?error=Выбери сделку",
            status_code=303
        )

    # current_user.id
    deal = db.query(Deal).filter(
        Deal.id == deal_id,
        Deal.user_id == current_user.id
    ).first()

    if deal:
        db.delete(deal)
        db.commit()

    return RedirectResponse("/deals", status_code=303)


@router.post("/update/{deal_id}")
def update_deal(
    request: Request,
    deal_id: int,
    asset: str = Form(None),
    direction: str = Form(None),
    amount: float = Form(None),
    entry_price: float = Form(None),
    exit_price: float = Form(None),
    date: str = Form(None),
    timeframe: str = Form(None),
    comment: str = Form(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not current_user: # Проверка токена
        return RedirectResponse("/auth-page")

    # Поиск сделки через current_user.id
    deal = db.query(Deal).filter(
        Deal.id == deal_id,
        Deal.user_id == current_user.id
    ).first()

    if not deal:
        return RedirectResponse("/deals")

    if not all([asset, direction, amount, entry_price, exit_price, date]):
        return RedirectResponse(
            "/deals?error=Заполни все поля",
            status_code=303
        )

    deal.asset = asset
    deal.direction = direction
    deal.amount = amount
    deal.entry_price = entry_price
    deal.exit_price = exit_price
    deal.date = datetime.strptime(date, "%Y-%m-%d").date()
    deal.timeframe = timeframe
    deal.comment = comment
    deal.profit = calculate_profit(direction, entry_price, exit_price, amount)

    db.commit()

    return RedirectResponse("/deals", status_code=303)