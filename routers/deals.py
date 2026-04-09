from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.deal import DealCreate, DealRead
from services.deal_service import create_deal, get_user_deals, delete_deal, update_deal
from utils.dependencies import get_current_user

router = APIRouter(
    prefix="/deals",
    tags=["Deals"]
)


@router.post("/")
def create_new_deal(
    deal: DealCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_deal(db, current_user.id, deal)


@router.get("/", response_model=List[DealRead])
def get_deals(
    asset: str = None,
    result: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    deals = get_user_deals(db, current_user.id)

    if asset:
        deals = [d for d in deals if d.asset == asset]

    if result:
        deals = [d for d in deals if d.result == result]

    return deals


@router.delete("/{deal_id}")
def delete_deal_endpoint(
    deal_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    deal = delete_deal(db, deal_id, current_user.id)

    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    return {"message": "Deal deleted"}


@router.put("/{deal_id}", response_model=DealRead)
def update_deal_endpoint(
    deal_id: int,
    deal: DealCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    updated = update_deal(db, deal_id, current_user.id, deal)

    if not updated:
        raise HTTPException(status_code=404, detail="Deal not found")
    
    return updated