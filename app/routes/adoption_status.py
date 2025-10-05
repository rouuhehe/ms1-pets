from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from datetime import datetime
from ..db import get_db
from ..models import AdoptionStatus, AdoptionState

router = APIRouter(prefix="/adoption-status", tags=["adoption_status"])

# -------------------------
# Helper
# -------------------------
def status_to_dict(status: AdoptionStatus):
    return {
        "id": str(status.id),
        "pet_id": str(status.pet_id),
        "state": status.state.value,
        "created_at": status.created_at.isoformat(),
        "last_updated": status.last_updated.isoformat() if status.last_updated else None,
    }

# -------------------------
# Schemas
# -------------------------
from pydantic import BaseModel

class AdoptionStatusCreate(BaseModel):
    pet_id: str
    state: str = "available"

class AdoptionStatusUpdate(BaseModel):
    state: str

# -------------------------
# Endpoints
# -------------------------
@router.post("/", response_model=dict)
def create_status(payload: AdoptionStatusCreate, db: Session = Depends(get_db)):
    status = AdoptionStatus(pet_id=payload.pet_id, state=AdoptionState[payload.state])
    db.add(status)
    db.commit()
    db.refresh(status)
    return status_to_dict(status)

@router.get("/{pet_id}", response_model=dict)
def get_status(pet_id: str, db: Session = Depends(get_db)):
    status = db.query(AdoptionStatus).filter(AdoptionStatus.pet_id == pet_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Adoption status not found")
    return status_to_dict(status)

@router.patch("/{pet_id}", response_model=dict)
def update_status(pet_id: str, payload: AdoptionStatusUpdate, db: Session = Depends(get_db)):
    status = db.query(AdoptionStatus).filter(AdoptionStatus.pet_id == pet_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Adoption status not found")
    status.state = AdoptionState[payload.state]
    db.commit()
    db.refresh(status)
    return status_to_dict(status)

@router.delete("/{pet_id}")
def delete_status(pet_id: str, db: Session = Depends(get_db)):
    status = db.query(AdoptionStatus).filter(AdoptionStatus.pet_id == pet_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Adoption status not found")
    db.delete(status)
    db.commit()
    return {"detail": "Deleted"}
