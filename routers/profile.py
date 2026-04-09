from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from utils.dependencies import get_current_user

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/")
def get_profile(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at
    }