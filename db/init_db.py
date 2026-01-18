from db.base import Base
from db.session import engine
from models.user import User
from models.deal import Deal

def init_db():
    '''
    Создание таблиц в базе данных, если их нет
    '''
    Base.metadata.create_all(bind = engine)


if __name__ == '__main__':
    init_db()