from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# подключение к базе данных
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://user:password@db:5432/investment_db"
)

# движок SQLAlchemy
engine = create_engine(DATABASE_URL)


# сессии
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        