from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID


class AdoptionCenterBase(BaseModel):
    name: str
    address: str
    city: str
    lat: Optional[float] = None
    lon: Optional[float] = None


class AdoptionCenterCreate(AdoptionCenterBase):
    pass


class AdoptionCenterUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class AdoptionCenterResponse(AdoptionCenterBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
