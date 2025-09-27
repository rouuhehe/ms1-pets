from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.db.session import get_db_session
from app.schemas import VaccineCreate, VaccineUpdate, VaccineResponse
from app.services import vaccine_service
from fastapi import Response

router = APIRouter(
    prefix="/vaccines",
    tags=["vaccines"],
)


@router.get("/", response_model=List[VaccineResponse])
def list_vaccines(
        db: Session = Depends(get_db_session),
        pet_id: Optional[UUID] = Query(None, description="Filtrar vacunas por mascota"),
):
    return vaccine_service.get_vaccines(db, pet_id=pet_id)


@router.get("/{vaccine_id}", response_model=VaccineResponse)
def get_vaccine(vaccine_id: UUID, db: Session = Depends(get_db_session)):
    vaccine = vaccine_service.get_vaccine_by_id(db, vaccine_id)
    if not vaccine:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    return vaccine


@router.post("/", response_model=VaccineResponse, status_code=201)
def create_vaccine(vaccine: VaccineCreate, db: Session = Depends(get_db_session)):
    return vaccine_service.create_vaccine(db, vaccine)


@router.patch("/{vaccine_id}", response_model=VaccineResponse)
def update_vaccine(vaccine_id: UUID, vaccine_update: VaccineUpdate, db: Session = Depends(get_db_session)):
    vaccine = vaccine_service.update_vaccine(db, vaccine_id, vaccine_update)
    if not vaccine:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    return vaccine


@router.delete("/{vaccine_id}")
def delete_vaccine(vaccine_id: UUID, db: Session = Depends(get_db_session)):
    success = vaccine_service.delete_vaccine(db, vaccine_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    return Response(status_code=204)