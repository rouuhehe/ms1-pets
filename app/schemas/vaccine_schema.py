from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional
from uuid import UUID


class VaccineBase(BaseModel):
    pet_id: UUID
    type: str
    date: date


class VaccineCreate(VaccineBase):
    pass


class VaccineUpdate(BaseModel):
    type: Optional[str] = None
    date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)


class VaccineResponse(VaccineBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
