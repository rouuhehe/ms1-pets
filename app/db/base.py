from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.adoption_center import AdoptionCenter
from app.models.pet import Pet
from app.models.adoption_status import AdoptionStatus
from app.models.vaccine import Vaccine