from sqlalchemy.orm import Session
from typing import Optional
from app.models.adoption_status import AdoptionStatus
from app.schemas import AdoptionStatusCreate, AdoptionStatusUpdate
from uuid import UUID


def get_adoption_status(db: Session, pet_id: UUID) -> Optional[AdoptionStatus]:
    return db.query(AdoptionStatus).filter(AdoptionStatus.pet_id == pet_id).first()


def create_adoption_status(db: Session, status: AdoptionStatusCreate) -> AdoptionStatus:
    db_status = AdoptionStatus(**status.model_dump())
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status


def update_adoption_status(
        db: Session, pet_id: UUID, status_update: AdoptionStatusUpdate
) -> Optional[AdoptionStatus]:
    from typing import cast

    db_status = db.query(AdoptionStatus).filter(AdoptionStatus.pet_id == pet_id).first()
    db_status = cast(Optional[AdoptionStatus], db_status)

    if not db_status:
        return None

    for key, value in status_update.model_dump(exclude_unset=True).items():
        setattr(db_status, key, value)

    db.commit()
    db.refresh(db_status)
    return db_status


def delete_adoption_status(db: Session, pet_id: UUID) -> bool:
    db_status = db.query(AdoptionStatus).filter(AdoptionStatus.pet_id == pet_id).first()
    if not db_status:
        return False

    db.delete(db_status)
    db.commit()
    return True
