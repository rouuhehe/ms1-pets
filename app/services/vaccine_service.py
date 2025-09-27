from sqlalchemy.orm import Session
from typing import Optional, List, Type
from uuid import UUID
from app.models.vaccine import Vaccine
from app.schemas import VaccineCreate, VaccineUpdate


def get_vaccines(db: Session, pet_id: Optional[UUID] = None, skip: int = 0, limit: int = 20) -> List[Type[Vaccine]]:
    query = db.query(Vaccine)
    if pet_id:
        query = query.filter(Vaccine.pet_id == pet_id)
    return list(query.offset(skip).limit(limit).all())


def get_vaccine_by_id(db: Session, vaccine_id: UUID) -> Optional[Vaccine]:
    return db.query(Vaccine).filter(Vaccine.id == vaccine_id).first()


def create_vaccine(db: Session, vaccine: VaccineCreate) -> Vaccine:
    db_vaccine = Vaccine(**vaccine.model_dump())
    db.add(db_vaccine)
    db.commit()
    db.refresh(db_vaccine)
    return db_vaccine


def update_vaccine(db: Session, vaccine_id: UUID, vaccine_update: VaccineUpdate) -> Optional[Type[Vaccine]]:
    db_vaccine = db.query(Vaccine).filter(Vaccine.id == vaccine_id).first()
    if not db_vaccine:
        return None

    for key, value in vaccine_update.model_dump(exclude_unset=True).items():
        setattr(db_vaccine, key, value)

    db.commit()
    db.refresh(db_vaccine)
    return db_vaccine


def delete_vaccine(db: Session, vaccine_id: UUID) -> bool:
    db_vaccine = db.query(Vaccine).filter(Vaccine.id == vaccine_id).first()
    if not db_vaccine:
        return False

    db.delete(db_vaccine)
    db.commit()
    return True
