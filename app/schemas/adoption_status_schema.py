from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.adoption_status import AdoptionState
from uuid import UUID


class AdoptionStatusBase(BaseModel):
    state: AdoptionState


class AdoptionStatusCreate(AdoptionStatusBase):
    pet_id: UUID


class AdoptionStatusUpdate(BaseModel):
    state: AdoptionState
    model_config = ConfigDict(from_attributes=True)


class AdoptionStatusResponse(AdoptionStatusBase):
    id: UUID
    pet_id: UUID
    last_updated: datetime

    model_config = ConfigDict(from_attributes=True)
