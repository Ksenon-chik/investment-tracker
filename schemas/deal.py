from pydantic import BaseModel
from datetime import datetime

class DealBase(BaseModel):
    asset: str
    amount: float
    price: float
    deal_type: str

class DealCreate(DealBase):
    pass

class DealRead(DealBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True