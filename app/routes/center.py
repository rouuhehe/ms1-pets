from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from ..db import get_db
from ..models import AdoptionCenter

router = APIRouter(prefix="/centers", tags=["centers"])

# -------------------------
# Helper
# -------------------------
def center_to_dict(center: AdoptionCenter):
    return {
        "id": str(center.id),
        "name": center.name,
        "address": center.address,
        "city": center.city,
        "lat": center.lat,
        "lon": center.lon,
    }

# -------------------------
# Schemas Pydantic
# -------------------------
from pydantic import BaseModel

class CenterCreate(BaseModel):
    name: str
    address: str
    city: str
    lat: Optional[float] = None
    lon: Optional[float] = None

class CenterUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None

# -------------------------
# Endpoints
# -------------------------
@router.post("/", response_model=dict)
def create_center(payload: CenterCreate, db: Session = Depends(get_db)):
    center = AdoptionCenter(
        name=payload.name,
        address=payload.address,
        city=payload.city,
        lat=payload.lat,
        lon=payload.lon
    )
    db.add(center)
    db.commit()
    db.refresh(center)
    return center_to_dict(center)

@router.get("/", response_model=List[dict])
def list_centers(db: Session = Depends(get_db)):
    centers = db.query(AdoptionCenter).all()
    return [center_to_dict(c) for c in centers]

@router.get("/{center_id}", response_model=dict)
def get_center(center_id: str, db: Session = Depends(get_db)):
    center = db.query(AdoptionCenter).filter(AdoptionCenter.id == center_id).first()
    if not center:
        raise HTTPException(status_code=404, detail="Center not found")
    return center_to_dict(center)

@router.patch("/{center_id}", response_model=dict)
def update_center(center_id: str, payload: CenterUpdate, db: Session = Depends(get_db)):
    center = db.query(AdoptionCenter).filter(AdoptionCenter.id == center_id).first()
    if not center:
        raise HTTPException(status_code=404, detail="Center not found")
    if payload.name: center.name = payload.name
    if payload.address: center.address = payload.address
    if payload.city: center.city = payload.city
    if payload.lat is not None: center.lat = payload.lat
    if payload.lon is not None: center.lon = payload.lon
    db.commit()
    db.refresh(center)
    return center_to_dict(center)

@router.delete("/{center_id}")
def delete_center(center_id: str, db: Session = Depends(get_db)):
    center = db.query(AdoptionCenter).filter(AdoptionCenter.id == center_id).first()
    if not center:
        raise HTTPException(status_code=404, detail="Center not found")
    db.delete(center)
    db.commit()
    return {"detail": "Deleted"}
