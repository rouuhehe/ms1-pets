from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional, List
from app.schemas.adoption_status_schema import AdoptionStatusResponse
from app.schemas.vaccine_schema import VaccineResponse
from uuid import UUID


class PetBase(BaseModel):
    name: str
    species: str
    breed: str
    birth_date: date
    adoption_center_id: UUID
    image_url: Optional[str] = None


class PetCreate(PetBase):
    pass


class PetUpdate(BaseModel):
    name: Optional[str] = None
    breed: Optional[str] = None
    adoption_center_id: Optional[UUID] = None
    image_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PetResponse(PetBase):
    id: UUID
    created_at: datetime
    adoption_status: Optional[AdoptionStatusResponse] = None
    vaccines: List[VaccineResponse] = []

    model_config = ConfigDict(from_attributes=True)
