from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base

class Deal(Base):
    __tablename__ = 'deals'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    asset = Column(String, nullable=False)
    direction = Column(String, nullable=False)  # buy / sell / long / short

    amount = Column(Float, nullable=False)

    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=False)

    profit = Column(Float, nullable=False)

    timeframe = Column(String, nullable=True)
    comment = Column(String, nullable=True)

    date = Column(Date, nullable=False)

    user = relationship("User", back_populates="deals")
    