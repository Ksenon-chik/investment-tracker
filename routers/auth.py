from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from db.session import get_db
from schemas.user import UserCreate
from services.user_service import create_user, authenticate_user, change_password

router = APIRouter(prefix="/auth", tags=["Auth"])

templates = Jinja2Templates(directory="templates")


# ================= REGISTER =================
@router.post("/register")
def register_form(
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    if password != confirm_password:
        return RedirectResponse(
            "/auth-page?error=Пароли не совпадают&mode=register",
            status_code=303
        )

    if len(password) < 6:
        return RedirectResponse(
            "/auth-page?error=Пароль слишком короткий&mode=register",
            status_code=303
        )

    try:
        user = create_user(db, UserCreate(email=email, password=password))

        response = RedirectResponse("/profile", status_code=303)
        response.set_cookie("user_id", str(user.id))
        return response

    except ValueError as e:
        return RedirectResponse(
            f"/auth-page?error={str(e)}&mode=register",
            status_code=303
        )


# ================= LOGIN =================
@router.post("/login-form")
def login_form(
    email: str = Form(None),
    password: str = Form(None),
    db: Session = Depends(get_db)
):
    if not email or not password:
        return RedirectResponse(
            "/auth-page?error=Заполни все поля",
            status_code=303
        )

    user = authenticate_user(db, email, password)

    if not user:
        return RedirectResponse(
            "/auth-page?error=Неверный email или пароль",
            status_code=303
        )

    response = RedirectResponse("/profile", status_code=303)
    response.set_cookie("user_id", str(user.id))
    return response


# ================= CHANGE PASSWORD =================
import re

@router.post("/change-password")
def change_user_password(
    request: Request,
    old_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    user_id = request.cookies.get("user_id")

    if not user_id:
        return RedirectResponse("/auth-page", status_code=303)

    # ❗ Проверка пустых полей
    if not old_password or not new_password or not confirm_password:
        return RedirectResponse(
            "/profile?error=Заполни все поля",
            status_code=303
        )

    # ❗ Совпадение паролей
    if new_password != confirm_password:
        return RedirectResponse(
            "/profile?error=Пароли не совпадают",
            status_code=303
        )

    # ❗ Минимальная длина
    if len(new_password) < 6:
        return RedirectResponse(
            "/profile?error=Пароль должен быть минимум 6 символов",
            status_code=303
        )

    # ❗ Сложность (буквы + цифры)
    if (
        not re.search(r"[A-Z]", new_password) or
        not re.search(r"[a-z]", new_password) or
        not re.search(r"\d", new_password)
    ):
        return RedirectResponse(
            "/profile?error=Пароль должен содержать заглавные, строчные буквы и цифры",
            status_code=303
    )

    try:
        change_password(
            db,
            int(user_id),
            old_password,
            new_password
        )

        return RedirectResponse(
            "/profile?success=Пароль успешно изменен",
            status_code=303
        )

    except ValueError as e:
        return RedirectResponse(
            f"/profile?error={str(e)}",
            status_code=303
        )