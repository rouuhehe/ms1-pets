from fastapi import APIRouter, HTTPException, Depends
from fastapi import Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from uuid import UUID
from ..db import get_db
from ..models import Pet

router = APIRouter(prefix="/pets", tags=["pets"])

# -------------------------
# Helper para serializar
# -------------------------
def pet_to_dict(pet: Pet):
    return {
        "id": str(pet.id),
        "name": pet.name,
        "species": pet.species,
        "breed": pet.breed,
        "birth_date": pet.birth_date.isoformat(),
        "adoption_center_id": str(pet.adoption_center_id),
        "image_url": pet.image_url,
    }

# -------------------------
# Schemas Pydantic simples
# -------------------------
from pydantic import BaseModel

class PetCreate(BaseModel):
    name: str
    species: str
    breed: str
    birth_date: date
    adoption_center_id: str

class PetUpdate(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    birth_date: Optional[date] = None

# -------------------------
# Endpoints
# -------------------------
@router.post("/", response_model=dict)
def create_pet(payload: PetCreate, db: Session = Depends(get_db)):
    pet = Pet(
        name=payload.name,
        species=payload.species,
        breed=payload.breed,
        birth_date=payload.birth_date,
        adoption_center_id=payload.adoption_center_id
    )
    db.add(pet)
    db.commit()
    db.refresh(pet)
    return pet_to_dict(pet)

@router.get("/", response_model=List[dict])
def list_pets(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros a retornar")
):
    total = db.query(Pet).count()
    pets = db.query(Pet).offset(skip).limit(limit).all()
    return {
        "total": total,
        "items": [pet_to_dict(p) for p in pets]
    }

@router.get("/{pet_id}", response_model=dict)
def get_pet(pet_id: str, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet_to_dict(pet)

@router.patch("/{pet_id}", response_model=dict)
def update_pet(pet_id: str, payload: PetUpdate, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    if payload.name: pet.name = payload.name
    if payload.species: pet.species = payload.species
    if payload.breed: pet.breed = payload.breed
    if payload.birth_date: pet.birth_date = payload.birth_date
    db.commit()
    db.refresh(pet)
    return pet_to_dict(pet)

@router.delete("/{pet_id}")
def delete_pet(pet_id: str, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    db.delete(pet)
    db.commit()
    return {"detail": "Deleted"}
