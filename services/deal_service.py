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
        date=deal_data.date,
        asset=deal_data.asset,
        direction=deal_data.direction,
        result=deal_data.result,
        amount=deal_data.amount,
        rr_ratio=deal_data.rr_ratio,
        comment=deal_data.comment,
        timeframe=deal_data.timeframe,
        price=deal_data.price
    )

    db.add(deal)
    db.commit()
    db.refresh(deal)

    return deal


def delete_deal(db: Session, deal_id: int, user_id: int):
    deal = db.query(Deal).filter(
        Deal.id == deal_id,
        Deal.user_id == user_id
    ).first()

    if not deal:
        return None
    
    db.delete(deal)
    db.commit()

    return deal


def update_deal(db: Session, deal_id: int, user_id: int, deal_data: DealCreate):
    deal = db.query(Deal).filter(
        Deal.id == deal_id,
        Deal.user_id == user_id
    ).first()

    if not deal:
        return None
    
    deal.asset = deal_data.asset
    deal.amount = deal_data.amount
    deal.price = deal_data.price
    deal.direction = deal_data.direction
    deal.result = deal_data.result
    deal.rr_ratio = deal_data.rr_ratio
    deal.comment = deal_data.comment
    deal.timeframe = deal_data.timeframe
    deal.date = deal_data.date

    db.commit()
    db.refresh(deal)

    return deal


def get_user_deals(db: Session, user_id: int) -> list[Deal]:
    return db.query(Deal).filter(Deal.user_id == user_id).all()