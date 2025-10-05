from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from ..db import get_db
from ..models import Pet
from pydantic import BaseModel
from uuid import UUID

router = APIRouter(prefix="/pets", tags=["pets"])

# Pydantic schemas para request/response
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

class PetResponse(BaseModel):
    id: UUID
    name: str
    species: str
    breed: str
    birth_date: date
    adoption_center_id: UUID
    image_url: Optional[str] = None

    class Config:
        orm_mode = True


@router.post("/", response_model=PetResponse)
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
    return pet


@router.get("/", response_model=List[PetResponse])
def list_pets(db: Session = Depends(get_db)):
    return db.query(Pet).all()


@router.get("/{pet_id}", response_model=PetResponse)
def get_pet(pet_id: str, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


@router.patch("/{pet_id}", response_model=PetResponse)
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
    return pet


@router.delete("/{pet_id}")
def delete_pet(pet_id: str, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    db.delete(pet)
    db.commit()
    return {"detail": "Deleted"}
