from sqlalchemy.orm import Session
from typing import List, Optional, Type
from uuid import UUID
from app.models.adoption_center import AdoptionCenter
from app.schemas import AdoptionCenterCreate, AdoptionCenterUpdate
from sqlalchemy import select


def get_centers(db: Session, skip: int = 0, limit: int = 20) -> List[Type[AdoptionCenter]]:
    return list(db.query(AdoptionCenter).offset(skip).limit(limit).all())


def get_center_by_id(db: Session, center_id: UUID) -> Optional[AdoptionCenter]:
    stmt = select(AdoptionCenter).where(AdoptionCenter.id == center_id)
    return db.execute(stmt).scalars().first()


def create_center(db: Session, center: AdoptionCenterCreate) -> AdoptionCenter:
    db_center = AdoptionCenter(**center.model_dump())
    db.add(db_center)
    db.commit()
    db.refresh(db_center)
    return db_center


def update_center(
        db: Session, center_id: UUID, center_update: AdoptionCenterUpdate
) -> Optional[AdoptionCenter]:
    db_center: Optional[AdoptionCenter] = (
        db.query(AdoptionCenter).filter(AdoptionCenter.id == center_id).first()
    )
    if not db_center:
        return None

    for key, value in center_update.model_dump(exclude_unset=True).items():
        setattr(db_center, key, value)

    db.commit()
    db.refresh(db_center)
    return db_center


def delete_center(db: Session, center_id: UUID) -> bool:
    db_center = db.query(AdoptionCenter).filter(AdoptionCenter.id == center_id).first()
    if not db_center:
        return False

    db.delete(db_center)
    db.commit()
    return True
