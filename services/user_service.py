from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from utils.security import hash_password, verify_password


def create_user(db: Session, user_data: UserCreate) -> User:
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        raise ValueError("Пользователь с таким email уже существует")

    user = User(
        email = user_data.email,
        hashed_password = hash_password(user_data.password),
        start_balance = user_data.start_balance
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    
    return user

from utils.security import verify_password, hash_password


def change_password(db: Session, user_id: int, old_password: str, new_password: str):
    user = get_user_by_id(db, user_id)

    if not user:
        raise ValueError("Пользователь не найден")

    # проверка старого пароля
    if not verify_password(old_password, user.hashed_password):
        raise ValueError("Неверный старый пароль")

    # валидация нового пароля
    if len(new_password) < 6:
        raise ValueError("Пароль должен быть минимум 6 символов")

    # обновление пароля
    user.hashed_password = hash_password(new_password)

    db.commit()
    db.refresh(user)

    return user