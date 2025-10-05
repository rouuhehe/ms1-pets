from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date as dt_date
from ..db import get_db
from ..models import Vaccine
from pydantic import BaseModel
from uuid import UUID

router = APIRouter(prefix="/vaccines", tags=["vaccines"])

# Pydantic schemas
class VaccineCreate(BaseModel):
    pet_id: str
    type: str
    date: dt_date

class VaccineUpdate(BaseModel):
    type: Optional[str] = None
    date: Optional[dt_date] = None

class VaccineResponse(BaseModel):
    id: UUID
    pet_id: UUID
    type: str
    date: dt_date

    class Config:
        from_attributes = True


@router.post("/", response_model=VaccineResponse)
def create_vaccine(payload: VaccineCreate, db: Session = Depends(get_db)):
    vac = Vaccine(pet_id=payload.pet_id, type=payload.type, date=payload.date)
    db.add(vac)
    db.commit()
    db.refresh(vac)
    return vac


@router.get("/", response_model=List[VaccineResponse])
def list_vaccines(db: Session = Depends(get_db)):
    return db.query(Vaccine).all()


@router.get("/{vaccine_id}", response_model=VaccineResponse)
def get_vaccine(vaccine_id: str, db: Session = Depends(get_db)):
    vac = db.query(Vaccine).filter(Vaccine.id == vaccine_id).first()
    if not vac:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    return vac


@router.patch("/{vaccine_id}", response_model=VaccineResponse)
def update_vaccine(vaccine_id: str, payload: VaccineUpdate, db: Session = Depends(get_db)):
    vac = db.query(Vaccine).filter(Vaccine.id == vaccine_id).first()
    if not vac:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    if payload.type: vac.type = payload.type
    if payload.date: vac.date = payload.date
    db.commit()
    db.refresh(vac)
    return vac


@router.delete("/{vaccine_id}")
def delete_vaccine(vaccine_id: str, db: Session = Depends(get_db)):
    vac = db.query(Vaccine).filter(Vaccine.id == vaccine_id).first()
    if not vac:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    db.delete(vac)
    db.commit()
    return {"detail": "Deleted"}
