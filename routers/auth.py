from fastapi import APIRouter, Depends, HTTPException, Form, Request # Группировка endpoints
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.user import UserCreate, UserResponse, UserLogin, ChangePassword
from services.user_service import create_user, authenticate_user, change_password
from utils.security import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from utils.dependencies import get_current_user
from fastapi.responses import RedirectResponse

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register")
def register_user(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        new_user = create_user(
            db,
            UserCreate(email=email, password=password)
        )

        response = RedirectResponse(url="/profile", status_code=302)
        response.set_cookie(key="user_id", value=str(new_user.id))

        return response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, email, password)

    if not user:
        return RedirectResponse("/auth-page", status_code=302)

    response = RedirectResponse(url="/profile", status_code=302)
    response.set_cookie(key="user_id", value=str(user.id))

    return response


@router.post("/change-password")
def change_user_password(
    request: Request,
    old_password: str = Form(...),
    new_password: str = Form(...),
    db: Session = Depends(get_db)
):
    user_id = request.cookies.get("user_id")

    if not user_id:
        return RedirectResponse("/auth-page")

    try:
        change_password(
            db,
            int(user_id),
            old_password,
            new_password
        )

        return RedirectResponse("/profile", status_code=302)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/login-form")
def login_form(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, email, password)

    if not user:
        return templates.TemplateResponse("auth.html", {
            "request": request,
            "error": "Неверный email или пароль"
        })

    response = RedirectResponse(url="/profile", status_code=302)
    response.set_cookie(key="user_id", value=str(user.id))

    return response