from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .auth import get_current_user
from db.session import get_db
from services.deal_service import get_user_deals, create_deal as create_deal_service
from datetime import datetime
from models.deal import Deal
from utils.calculations import calculate_profit

router = APIRouter(
    prefix="/deals",
    tags=["Deals"]
)

templates = Jinja2Templates(directory="templates")


# Страница сделок
@router.get("/", response_class=HTMLResponse)
def deals_page(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")

    if not user_id:
        return RedirectResponse("/auth-page")

    deals = get_user_deals(db, int(user_id))

    return templates.TemplateResponse("deals.html", {
        "request": request,
        "deals": deals
    })


# Создание сделки (из формы)
@router.post("/create")
def create_deal(
    request: Request,
    asset: str = Form(...),
    direction: str = Form(...),
    amount: float = Form(...),
    entry_price: float = Form(...),
    exit_price: float = Form(...),
    date: str = Form(...),
    timeframe: str = Form(None),
    comment: str = Form(None),
    db: Session = Depends(get_db)
):
    user_id = request.cookies.get("user_id")

    if not user_id:
        return RedirectResponse("/auth-page")

    date_obj = datetime.strptime(date, "%Y-%m-%d").date()

    profit = calculate_profit(direction, entry_price, exit_price, amount)

    deal = Deal(
        user_id=int(user_id),
        asset=asset,
        direction=direction,
        amount=amount,
        entry_price=entry_price,
        exit_price=exit_price,
        profit=profit,
        timeframe=timeframe,
        comment=comment,
        date=date_obj
    )

    db.add(deal)
    db.commit()

    return RedirectResponse("/deals", status_code=302)


# Удаление сделки
@router.post("/delete/{deal_id}")
def delete_deal(
    request: Request,
    deal_id: int,
    db: Session = Depends(get_db)
):
    user_id = request.cookies.get("user_id")

    if not user_id:
        return RedirectResponse("/auth-page")

    from services.deal_service import delete_deal as delete_deal_service

    delete_deal_service(db, deal_id, int(user_id))

    return RedirectResponse("/deals", status_code=302)


@router.post("/delete-selected")
def delete_selected(
    request: Request,
    deal_id: int = Form(...),
    db: Session = Depends(get_db)
):
    user_id = request.cookies.get("user_id")

    if not user_id:
        return RedirectResponse("/auth-page")

    deal = db.query(Deal).filter(
        Deal.id == deal_id,
        Deal.user_id == int(user_id)
    ).first()

    if deal:
        db.delete(deal)
        db.commit()

    return RedirectResponse("/deals", status_code=302)


# Обновление сделки
@router.post("/update/{deal_id}")
def update_deal(
    request: Request,
    deal_id: int,
    asset: str = Form(...),
    direction: str = Form(...),
    amount: float = Form(...),
    entry_price: float = Form(...),
    exit_price: float = Form(...),
    date: str = Form(...),
    timeframe: str = Form(None),
    comment: str = Form(None),
    db: Session = Depends(get_db)
):
    user_id = request.cookies.get("user_id")

    deal = db.query(Deal).filter(
        Deal.id == deal_id,
        Deal.user_id == int(user_id)
    ).first()

    if not deal:
        return RedirectResponse("/deals")

    date_obj = datetime.strptime(date, "%Y-%m-%d").date()

    deal.asset = asset
    deal.direction = direction
    deal.amount = amount
    deal.entry_price = entry_price
    deal.exit_price = exit_price
    deal.timeframe = timeframe
    deal.comment = comment
    deal.date = date_obj
    deal.profit = calculate_profit(direction, entry_price, exit_price, amount)

    db.commit()

    return RedirectResponse("/deals", status_code=302)