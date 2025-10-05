from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import AdoptionStatus, AdoptionState
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/adoption-status", tags=["adoption_status"])

class AdoptionStatusCreate(BaseModel):
    pet_id: str
    state: str = "available"

class AdoptionStatusUpdate(BaseModel):
    state: str

class AdoptionStatusResponse(BaseModel):
    id: UUID
    pet_id: UUID
    state: str
    created_at: datetime
    last_updated: Optional[datetime] = None

    class Config:
        from_attributes = True

@router.post("/", response_model=AdoptionStatusResponse)
def create_status(payload: AdoptionStatusCreate, db: Session = Depends(get_db)):
    status = AdoptionStatus(pet_id=payload.pet_id, state=AdoptionState[payload.state])
    db.add(status)
    db.commit()
    db.refresh(status)
    return status

@router.get("/{pet_id}", response_model=AdoptionStatusResponse)
def get_status(pet_id: str, db: Session = Depends(get_db)):
    status = db.query(AdoptionStatus).filter(AdoptionStatus.pet_id == pet_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Adoption status not found")
    return status

@router.patch("/{pet_id}", response_model=AdoptionStatusResponse)
def update_status(pet_id: str, payload: AdoptionStatusUpdate, db: Session = Depends(get_db)):
    status = db.query(AdoptionStatus).filter(AdoptionStatus.pet_id == pet_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Adoption status not found")
    status.state = AdoptionState[payload.state]
    db.commit()
    db.refresh(status)
    return status

@router.delete("/{pet_id}")
def delete_status(pet_id: str, db: Session = Depends(get_db)):
    status = db.query(AdoptionStatus).filter(AdoptionStatus.pet_id == pet_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Adoption status not found")
    db.delete(status)
    db.commit()
    return {"detail": "Deleted"}
