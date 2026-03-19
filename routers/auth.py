from fastapi import APIRouter, Depends # Группировка endpoints
from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.session import get_db
from schemas.user import UserCreate, UserResponse, UserLogin
from services.user_service import create_user, authenticate_user
from utils.security import create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register", response_model=UserResponse)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    new_user = create_user(db, user)
    return new_user

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)

    if not db_user:
        raise HTTPException(status_code=401, detail="Inavalid credentials")
    
    token = create_access_token({"sub": str(db_user.id)})

    return {"access_token": token, "token_type": "bearer"}