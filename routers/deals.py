from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.deal import DealCreate
from services.deal_service import create_deal
from utils.dependencies import get_current_user

router = APIRouter(
    prefix="/deals",
    tags=["Deals"]
)


@router.post("/")
def create_new_deal(
    deal: DealCreate,
    token: str,
    db: Session = Depends(get_db),
):
    current_user = get_current_user(token, db)
    return create_deal(db, current_user.id, deal)