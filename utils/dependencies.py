from fastapi import Request, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from db.session import get_db
from models.user import User
from utils.security import SECRET_KEY, ALGORITHM


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    token = request.cookies.get("access_token")

    if not token:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))

        if user_id is None:
            return None
        user_id = int(user_id)
    except (JWTError, ValueError):
        return None

    user = db.query(User).filter(User.id == user_id).first()

    return user