from sqlalchemy import Column, Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, MappedColumn, mapped_column
from app.db.base import Base
import uuid

class Vaccine(Base):
    __tablename__ = "vaccine"

    id: MappedColumn[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pet.id"), nullable=False)
    type = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)

    # Relación N:1 -> una vacuna pertenece a una mascota
    pet = relationship("Pet", back_populates="vaccines")

    def __repr__(self):
        return (f"<Vaccine("
                
                f"id={self.id}, "
                f"type='{self.type}', "
                f"date={self.date}, "
                f"pet_id={self.pet_id})>")
