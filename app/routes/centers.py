from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.db.session import get_db_session
from app.schemas import AdoptionCenterCreate, AdoptionCenterUpdate, AdoptionCenterResponse
from app.services import adoption_center_service

router = APIRouter(
    prefix="/centers",
    tags=["centers"],
)


@router.get("/", response_model=List[AdoptionCenterResponse])
def list_centers(db: Session = Depends(get_db_session)):
    return adoption_center_service.get_centers(db)


@router.get("/{center_id}", response_model=AdoptionCenterResponse)
def get_center(center_id: UUID, db: Session = Depends(get_db_session)):
    center = adoption_center_service.get_center_by_id(db, center_id)
    if not center:
        raise HTTPException(status_code=404, detail="Center not found")
    return center


@router.post("/", response_model=AdoptionCenterResponse, status_code=201)
def create_center(center: AdoptionCenterCreate, db: Session = Depends(get_db_session)):
    return adoption_center_service.create_center(db, center)


@router.patch("/{center_id}", response_model=AdoptionCenterResponse)
def update_center(center_id: UUID, center_update: AdoptionCenterUpdate, db: Session = Depends(get_db_session)):
    center = adoption_center_service.update_center(db, center_id, center_update)
    if not center:
        raise HTTPException(status_code=404, detail="Center not found")
    return center


@router.delete("/{center_id}", status_code=204)
def delete_center(center_id: UUID, db: Session = Depends(get_db_session)):
    success = adoption_center_service.delete_center(db, center_id)
    if not success:
        raise HTTPException(status_code=404, detail="Center not found")
    return None
