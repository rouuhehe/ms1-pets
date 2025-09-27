import enum
import uuid
from datetime import datetime, UTC
from sqlalchemy import Column, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship, MappedColumn, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class AdoptionState(enum.Enum):
    available = "available"
    in_process = "in_process"
    adopted = "adopted"


class AdoptionStatus(Base):
    __tablename__ = "adoption_status"

    id: MappedColumn[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pet.id"), nullable=False, unique=True)
    state = Column(Enum(AdoptionState), nullable=False, default=AdoptionState.available)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    last_updated = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    # Relación 1:1 -> cada mascota tiene un estado de adopción único
    pet = relationship("Pet", back_populates="adoption_status")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.state is None:
            self.state = AdoptionState.available
        if self.last_updated is None:
            self.last_updated = datetime.now(UTC)


    def __repr__(self):
        return (
            f"<AdoptionStatus("
            
            f"pet_id={self.pet_id}, "
            f"state={self.state.name}, "
            f"last_updated={self.last_updated})>"
        )
