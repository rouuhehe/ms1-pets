from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date as dt_date
from uuid import UUID
from ..db import get_db
from ..models import Vaccine

router = APIRouter(prefix="/vaccines", tags=["vaccines"])

# -------------------------
# Helper
# -------------------------
def vaccine_to_dict(vac: Vaccine):
    return {
        "id": str(vac.id),
        "pet_id": str(vac.pet_id),
        "type": vac.type,
        "date": vac.date.isoformat(),
    }

# -------------------------
# Schemas
# -------------------------
from pydantic import BaseModel

class VaccineCreate(BaseModel):
    pet_id: str
    type: str
    date: dt_date

class VaccineUpdate(BaseModel):
    type: Optional[str] = None
    date: Optional[dt_date] = None

# -------------------------
# Endpoints
# -------------------------
@router.post("/", response_model=dict)
def create_vaccine(payload: VaccineCreate, db: Session = Depends(get_db)):
    vac = Vaccine(pet_id=payload.pet_id, type=payload.type, date=payload.date)
    db.add(vac)
    db.commit()
    db.refresh(vac)
    return vaccine_to_dict(vac)

@router.get("/", response_model=List[dict])
def list_vaccines(db: Session = Depends(get_db)):
    vacs = db.query(Vaccine).all()
    return [vaccine_to_dict(v) for v in vacs]

@router.get("/{vaccine_id}", response_model=dict)
def get_vaccine(vaccine_id: str, db: Session = Depends(get_db)):
    vac = db.query(Vaccine).filter(Vaccine.id == vaccine_id).first()
    if not vac:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    return vaccine_to_dict(vac)

@router.patch("/{vaccine_id}", response_model=dict)
def update_vaccine(vaccine_id: str, payload: VaccineUpdate, db: Session = Depends(get_db)):
    vac = db.query(Vaccine).filter(Vaccine.id == vaccine_id).first()
    if not vac:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    if payload.type: vac.type = payload.type
    if payload.date: vac.date = payload.date
    db.commit()
    db.refresh(vac)
    return vaccine_to_dict(vac)

@router.delete("/{vaccine_id}")
def delete_vaccine(vaccine_id: str, db: Session = Depends(get_db)):
    vac = db.query(Vaccine).filter(Vaccine.id == vaccine_id).first()
    if not vac:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    db.delete(vac)
    db.commit()
    return {"detail": "Deleted"}
