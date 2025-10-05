import uuid
from sqlalchemy import Column, String, Date, DateTime, Float, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
import enum

Base = declarative_base()

# ----------------------
# Centros de adopción
# ----------------------
class AdoptionCenter(Base):
    __tablename__ = "adoption_centers"
    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)

    # Relación con mascotas
    pets = relationship("Pet", back_populates="adoption_center", cascade="all, delete-orphan")


# ----------------------
# Mascotas
# ----------------------
class Pet(Base):
    __tablename__ = "pet"
    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    species = Column(String(50), nullable=False)
    breed = Column(String(50), nullable=False)
    birth_date = Column(Date, nullable=False)
    adoption_center_id = Column(PGUUID(as_uuid=True), ForeignKey("adoption_centers.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    image_url = Column(String(255), nullable=True)

    # Relaciones
    adoption_center = relationship("AdoptionCenter", back_populates="pets")
    adoption_status = relationship("AdoptionStatus", back_populates="pet", uselist=False)
    vaccines = relationship("Vaccine", back_populates="pet", cascade="all, delete-orphan")


# ----------------------
# Estado de adopción
# ----------------------
class AdoptionState(enum.Enum):
    AVAILABLE = "AVAILABLE"
    IN_PROCESS = "IN_PROCESS"
    ADOPTED = "ADOPTED"


class AdoptionStatus(Base):
    __tablename__ = "adoption_status"
    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id = Column(PGUUID(as_uuid=True), ForeignKey("pet.id"), nullable=False, unique=True)
    state = Column(Enum(AdoptionState), nullable=False, default=AdoptionState.available)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relación inversa
    pet = relationship("Pet", back_populates="adoption_status")


# ----------------------
# Vacunas
# ----------------------
class Vaccine(Base):
    __tablename__ = "vaccines"  # <--- aquí va con “s” para que coincida con la DB
    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id = Column(PGUUID(as_uuid=True), ForeignKey("pet.id"), nullable=False)
    type = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)

    # Relación inversa
    pet = relationship("Pet", back_populates="vaccines")
