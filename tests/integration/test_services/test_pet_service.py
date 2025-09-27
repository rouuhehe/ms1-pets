import uuid
import datetime
import pytest
from sqlalchemy.orm import Session
from app.schemas.pet_schema import PetCreate, PetUpdate
from app.services import pet_service


@pytest.fixture
def sample_pet_data():
    return PetCreate(
        name="Firulais",
        species="Dog",
        breed="Labrador",
        birth_date=datetime.date(2020, 1, 1),
        adoption_center_id=uuid.uuid4(),
    )


def test_create_pet(db_session: Session, sample_pet_data):
    pet = pet_service.create_pet(db_session, sample_pet_data)
    assert pet.id is not None
    assert pet.name == "Firulais"
    assert pet.species == "Dog"
    assert pet.breed == "Labrador"
    assert isinstance(pet.birth_date, datetime.date)


def test_get_pet_by_id(db_session: Session, sample_pet_data):
    created_pet = pet_service.create_pet(db_session, sample_pet_data)
    fetched_pet = pet_service.get_pet_by_id(db_session, created_pet.id)
    assert fetched_pet is not None
    assert fetched_pet.id == created_pet.id


def test_update_pet(db_session: Session, sample_pet_data):
    created_pet = pet_service.create_pet(db_session, sample_pet_data)
    update_data = PetUpdate(name="Max", breed="Golden Retriever")
    updated_pet = pet_service.update_pet(db_session, created_pet.id, update_data)
    assert updated_pet is not None
    assert updated_pet.name == "Max"
    assert updated_pet.breed == "Golden Retriever"


def test_update_pet_not_found(db_session: Session):
    fake_id = uuid.uuid4()
    update_data = PetUpdate(name="Ghost")
    result = pet_service.update_pet(db_session, fake_id, update_data)
    assert result is None


def test_delete_pet(db_session: Session, sample_pet_data):
    created_pet = pet_service.create_pet(db_session, sample_pet_data)
    deleted = pet_service.delete_pet(db_session, created_pet.id)
    assert deleted is True
    assert pet_service.get_pet_by_id(db_session, created_pet.id) is None


def test_delete_pet_not_found(db_session: Session):
    fake_id = uuid.uuid4()
    deleted = pet_service.delete_pet(db_session, fake_id)
    assert deleted is False
