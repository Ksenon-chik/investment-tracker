from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from utils.security import hash_password


def create_user(db: Session, user_data: UserCreate) -> User:
    user = User(
        email = user_data.email,
        hashed_password = hash_password(user_data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user