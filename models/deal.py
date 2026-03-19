from sqlalchemy import(
    Column,
    Integer,
    String,
    Date,
    Float,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from db.base import Base

class Deal(Base):
    __tablename__ = 'deals'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    asset = Column(String, nullable=False)
    direction = Column(String, nullable=False)
    result = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    rr_ratio = Column(Float, nullable=True)
    comment = Column(String, nullable=True)
    timeframe = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user = relationship("User", back_populates="deals")
