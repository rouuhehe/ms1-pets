from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, MappedColumn, mapped_column
from app.db.base import Base
import uuid


class AdoptionCenter(Base):
    __tablename__ = "adoption_center"

    id: MappedColumn[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    name = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)

    # Relación 1:N -> un centro de adopción tiene muchas mascotas
    pets = relationship("Pet", back_populates="adoption_center")
