from sqlalchemy import Column, String, ForeignKey, DateTime, Index, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column, MappedColumn
from app.db.base import Base
from datetime import datetime, UTC, date
import uuid


class Pet(Base):
    __tablename__ = "pet"

    id: MappedColumn[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    name = Column(String(50), nullable=False, index=True)
    species = Column(String(50), nullable=False)
    breed = Column(String(50), nullable=False)
    birth_date = Column(Date, nullable=False)
    adoption_center_id = Column(UUID(as_uuid=True), ForeignKey("adoption_center.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False, index=True)
    image_url = Column(String(255), nullable=True)

    # Relaciones
    adoption_center = relationship("AdoptionCenter", back_populates="pets")
    vaccines = relationship("Vaccine", back_populates="pet", cascade="all, delete-orphan")
    adoption_status = relationship("AdoptionStatus", back_populates="pet", uselist=False)

    __table_args__ = (
        Index("idx_pet_species_birthdate", "species", "birth_date"),
        Index("idx_pet_center", "adoption_center_id"),
    )

    def __repr__(self):
        return (f"<Pet("
                f"id={self.id}, "
                f"name='{self.name}', "
                f"species='{self.species}', "
                f"breed='{self.breed}')>")

    @property
    def age(self) -> str:
        today = date.today()
        months = (today.year - self.birth_date.year) * 12 + (today.month - self.birth_date.month)

        if months < 12:
            return f"{months} months"
        else:
            years = months // 12
            return f"{years} years"

    @property
    def age_category(self) -> str:
        today = date.today()
        years = today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

        if years < 1:
            return "puppy"
        elif 1 <= years <= 7:
            return "adult"
        return "senior"
