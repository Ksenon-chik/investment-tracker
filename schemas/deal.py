from pydantic import BaseModel, field_validator
from datetime import datetime

class DealBase(BaseModel):
    date: datetime
    asset: str
    direction: str
    amount: float
    entry_price: float
    exit_price: float
    rr_ratio: float | None = None
    comment: str | None = None
    timeframe: str | None = None

class DealCreate(DealBase):
    @field_validator("amount")
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError("Объем сделки должен быть больше 0")
        return value

class DealRead(DealBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True