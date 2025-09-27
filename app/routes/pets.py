from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Any, Optional, Dict
from uuid import UUID
from app.db.session import get_db_session
from app.schemas import PetCreate, PetUpdate, PetResponse
from app.services import pet_service
from app.utils.paginator import paginate_query

router = APIRouter(
    prefix="/pets",
    tags=["pets"],
)


@router.get("/", response_model=Dict[str, Any])
def list_pets(
        db: Session = Depends(get_db_session),
        species: Optional[str] = Query(None, description="Species ID"),
        breed: Optional[str] = Query(None, description="Breed ID"),
        center_id: Optional[UUID] = Query(None, description="Adoption Center ID"),
        min_age: Optional[int] = Query(None, description="Min age in years"),
        max_age: Optional[int] = Query(None, description="Max age in years"),
        age_category: Optional[str] = Query(None, description="puppy, adult, senior"),
        page: int = Query(1, description="Page number"),
        page_size: int = Query(16, description="Results per page"),
):
    query = pet_service.get_pets_query(
        db,
        species=species,
        breed=breed,
        center_id=center_id,
        min_age=min_age,
        max_age=max_age,
        age_category=age_category,
    )

    return paginate_query(query, page=page, page_size=page_size)


@router.get("/{pet_id}", response_model=PetResponse)
def get_pet(pet_id: UUID, db: Session = Depends(get_db_session)):
    pet = pet_service.get_pet_by_id(db, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


@router.post("/", response_model=PetResponse, status_code=201)
def create_pet(pet: PetCreate, db: Session = Depends(get_db_session)):
    return pet_service.create_pet(db, pet)


@router.patch("/{pet_id}", response_model=PetResponse)
def update_pet(pet_id: UUID, pet_update: PetUpdate, db: Session = Depends(get_db_session)):
    pet = pet_service.update_pet(db, pet_id, pet_update)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


@router.delete("/{pet_id}", status_code=204)
def delete_pet(pet_id: UUID, db: Session = Depends(get_db_session)):
    success = pet_service.delete_pet(db, pet_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pet not found")
    return None
