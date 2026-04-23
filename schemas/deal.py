from pydantic import BaseModel
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
    pass


class DealRead(DealBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True