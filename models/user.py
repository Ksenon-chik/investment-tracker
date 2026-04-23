from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base
from .deal import Deal


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    start_balance = Column(Float, default=0.0)

    created_at = Column(DateTime, default=datetime.utcnow)
    deals = relationship('Deal', back_populates='user', cascade='all, delete')

    @property
    def total_capital(self):

        # Подсчет суммы всех profit из таблицы deals
        deals_profit = sum(deal.profit for deal in self.deals) if self.deals else 0.0
        return self.start_balance + deals_profit