from sqlalchemy.orm import Session
from models.deal import Deal
from schemas.deal import DealCreate


def create_deal(
    db: Session,
    user_id: int,
    deal_data: DealCreate
) -> Deal:
    deal = Deal(
        user_id=user_id,
        asset=deal_data.asset,
        amount=deal_data.amount,
        price=deal_data.price,
        deal_type=deal_data.deal_type
    )

    db.add(deal)
    db.commit()
    db.refresh(deal)

    return deal
