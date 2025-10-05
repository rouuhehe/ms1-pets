import uuid
from sqlalchemy import Column, String, Date, DateTime, Float, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
import enum

Base = declarative_base()

class AdoptionCenter(Base):
    __tablename__ = "adoption_center"
    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    pets = relationship("Pet", back_populates="adoption_center")

class Pet(Base):
    __tablename__ = "pet"
    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    species = Column(String(50), nullable=False)
    breed = Column(String(50), nullable=False)
    birth_date = Column(Date, nullable=False)
    adoption_center_id = Column(PGUUID(as_uuid=True), ForeignKey("adoption_center.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    image_url = Column(String(255), nullable=True)
    adoption_center = relationship("AdoptionCenter", back_populates="pets")
    adoption_status = relationship("AdoptionStatus", back_populates="pet", uselist=False)
    vaccines = relationship("Vaccine", back_populates="pet", cascade="all, delete-orphan")

class AdoptionState(enum.Enum):
    available = "available"
    in_process = "in_process"
    adopted = "adopted"

class AdoptionStatus(Base):
    __tablename__ = "adoption_status"
    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id = Column(PGUUID(as_uuid=True), ForeignKey("pet.id"), nullable=False, unique=True)
    state = Column(Enum(AdoptionState), nullable=False, default=AdoptionState.available)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    pet = relationship("Pet", back_populates="adoption_status")

class Vaccine(Base):
    __tablename__ = "vaccine"
    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id = Column(PGUUID(as_uuid=True), ForeignKey("pet.id"), nullable=False)
    type = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    pet = relationship("Pet", back_populates="vaccines")
