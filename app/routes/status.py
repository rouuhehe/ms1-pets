from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.session import get_db_session
from app.schemas import AdoptionStatusCreate, AdoptionStatusUpdate, AdoptionStatusResponse
from app.services import adoption_status_service

router = APIRouter(
    prefix="/adoption-status",
    tags=["adoption_status"],
)


@router.get("/{pet_id}", response_model=AdoptionStatusResponse)
def get_status(pet_id: UUID, db: Session = Depends(get_db_session)):
    status = adoption_status_service.get_adoption_status(db, pet_id)
    if not status:
        raise HTTPException(status_code=404, detail="Adoption status not found")
    return status


@router.post("/", response_model=AdoptionStatusResponse, status_code=201)
def create_status(status: AdoptionStatusCreate, db: Session = Depends(get_db_session)):
    return adoption_status_service.create_adoption_status(db, status)


@router.patch("/{pet_id}", response_model=AdoptionStatusResponse)
def update_status(pet_id: UUID, status_update: AdoptionStatusUpdate, db: Session = Depends(get_db_session)):
    status = adoption_status_service.update_adoption_status(db, pet_id, status_update)
    if not status:
        raise HTTPException(status_code=404, detail="Adoption status not found")
    return status


@router.delete("/{pet_id}", status_code=204)
def delete_status(pet_id: UUID, db: Session = Depends(get_db_session)):
    success = adoption_status_service.delete_adoption_status(db, pet_id)
    if not success:
        raise HTTPException(status_code=404, detail="Adoption status not found")
    return None
