from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from ..db import get_db
from ..models import AdoptionCenter
from pydantic import BaseModel
from uuid import UUID

router = APIRouter(prefix="/centers", tags=["centers"])

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

class CenterResponse(BaseModel):
    id: UUID
    name: str
    address: str
    city: str
    lat: Optional[float] = None
    lon: Optional[float] = None

    class Config:
        from_attributes = True


@router.post("/", response_model=CenterResponse)
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
    return center


@router.get("/", response_model=List[CenterResponse])
def list_centers(db: Session = Depends(get_db)):
    return db.query(AdoptionCenter).all()


@router.get("/{center_id}", response_model=CenterResponse)
def get_center(center_id: str, db: Session = Depends(get_db)):
    center = db.query(AdoptionCenter).filter(AdoptionCenter.id == center_id).first()
    if not center:
        raise HTTPException(status_code=404, detail="Center not found")
    return center


@router.patch("/{center_id}", response_model=CenterResponse)
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
    return center


@router.delete("/{center_id}")
def delete_center(center_id: str, db: Session = Depends(get_db)):
    center = db.query(AdoptionCenter).filter(AdoptionCenter.id == center_id).first()
    if not center:
        raise HTTPException(status_code=404, detail="Center not found")
    db.delete(center)
    db.commit()
    return {"detail": "Deleted"}
