from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List, Type
from datetime import date
from uuid import UUID

from app.models.pet import Pet
from app.schemas import PetCreate, PetUpdate


def get_pets(
        db: Session,
        species: Optional[str] = None,
        breed: Optional[str] = None,
        center_id: Optional[UUID] = None,
        min_age: Optional[int] = None,
        max_age: Optional[int] = None,
        age_category: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
) -> List[Type[Pet]]:
    """
    Devuelve lista de mascotas con filtros opcionales
    """
    query = db.query(Pet)

    if species:
        query = query.filter(Pet.species == species)
    if breed:
        query = query.filter(Pet.breed == breed)
    if center_id:
        query = query.filter(Pet.adoption_center_id == center_id)

    today = date.today()
    if min_age:
        cutoff = date(today.year - min_age, today.month, today.day)
        query = query.filter(Pet.birth_date <= cutoff)
    if max_age:
        cutoff = date(today.year - max_age, today.month, today.day)
        query = query.filter(Pet.birth_date >= cutoff)

    if age_category:
        if age_category == "puppy":
            cutoff = date(today.year - 1, today.month, today.day)
            query = query.filter(Pet.birth_date >= cutoff)
        elif age_category == "adult":
            cutoff_young = date(today.year - 7, today.month, today.day)
            cutoff_old = date(today.year - 1, today.month, today.day)
            query = query.filter(and_(Pet.birth_date < cutoff_old,
                                      Pet.birth_date >= cutoff_young))
        elif age_category == "senior":
            cutoff = date(today.year - 7, today.month, today.day)
            query = query.filter(Pet.birth_date < cutoff)

    return query.offset(skip).limit(limit).all()


def get_pets_query(
        db: Session,
        species: Optional[str] = None,
        breed: Optional[str] = None,
        center_id: Optional[UUID] = None,
        min_age: Optional[int] = None,
        max_age: Optional[int] = None,
        age_category: Optional[str] = None,
):
    """
    Devuelve un query filtrado de mascotas (sin paginar).
    """
    query = db.query(Pet)

    if species:
        query = query.filter(Pet.species == species)
    if breed:
        query = query.filter(Pet.breed == breed)
    if center_id:
        query = query.filter(Pet.adoption_center_id == center_id)

    today = date.today()
    if min_age:
        cutoff = date(today.year - min_age, today.month, today.day)
        query = query.filter(Pet.birth_date <= cutoff)
    if max_age:
        cutoff = date(today.year - max_age, today.month, today.day)
        query = query.filter(Pet.birth_date >= cutoff)

    if age_category:
        if age_category == "puppy":
            cutoff = date(today.year - 1, today.month, today.day)
            query = query.filter(Pet.birth_date >= cutoff)
        elif age_category == "adult":
            cutoff_young = date(today.year - 7, today.month, today.day)
            cutoff_old = date(today.year - 1, today.month, today.day)
            query = query.filter(and_(Pet.birth_date < cutoff_old, Pet.birth_date >= cutoff_young))
        elif age_category == "senior":
            cutoff = date(today.year - 7, today.month, today.day)
            query = query.filter(Pet.birth_date < cutoff)

    return query


def get_pet_by_id(db: Session, pet_id: UUID) -> Optional[Pet]:
    return db.query(Pet).filter(Pet.id == pet_id).first()


def create_pet(db: Session, pet: PetCreate) -> Pet:
    db_pet = Pet(**pet.model_dump())
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet


def update_pet(db: Session, pet_id: UUID, pet_update: PetUpdate) -> Optional[Type[Pet]]:
    db_pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not db_pet:
        return None

    for key, value in pet_update.model_dump(exclude_unset=True).items():
        setattr(db_pet, key, value)

    db.commit()
    db.refresh(db_pet)
    return db_pet


def delete_pet(db: Session, pet_id: UUID) -> bool:
    db_pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not db_pet:
        return False

    db.delete(db_pet)
    db.commit()
    return True
