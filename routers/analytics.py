from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from utils.dependencies import get_current_user
from services.analytics_service import (
    get_user_summary,
    get_full_analytics
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/")
def analytics(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return {
        "summary": get_user_summary(db, current_user.id),
        "advanced": get_full_analytics(db, current_user.id)
    }