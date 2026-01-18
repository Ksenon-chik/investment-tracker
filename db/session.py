from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# подключение к базе данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./investment_tracker.db"

# движок SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args = {'check_same_thread': False}
)


# session
SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)