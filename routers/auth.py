from fastapi import APIRouter, Depends, HTTPException # Группировка endpoints
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.user import UserCreate, UserResponse, UserLogin, ChangePassword
from services.user_service import create_user, authenticate_user, change_password
from utils.security import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from utils.dependencies import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

from schemas.user import ChangePassword
from services.user_service import change_password
from utils.dependencies import get_current_user


@router.post("/change-password")
def change_user_password(
    data: ChangePassword,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        change_password(
            db,
            current_user.id,
            data.old_password,
            data.new_password
        )
        return {"message": "Пароль успешно изменен"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))