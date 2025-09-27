import datetime
import uuid
from app.services import adoption_status_service
from app.schemas import AdoptionStatusCreate, AdoptionStatusUpdate
from app.models.adoption_status import AdoptionState


def test_create_adoption_status(db_session):
    pet_uuid = uuid.uuid4()
    schema = AdoptionStatusCreate(pet_id=pet_uuid, state=AdoptionState.available)
    status = adoption_status_service.create_adoption_status(db_session, schema)

    assert status.id is not None
    assert status.pet_id == pet_uuid
    assert status.state == AdoptionState.available
    assert isinstance(status.last_updated, datetime.datetime)


def test_get_adoption_status(db_session):
    pet_uuid = uuid.uuid4()
    schema = AdoptionStatusCreate(pet_id=pet_uuid, state=AdoptionState.in_process)
    created = adoption_status_service.create_adoption_status(db_session, schema)

    found = adoption_status_service.get_adoption_status(db_session, pet_uuid)
    assert found is not None
    assert found.pet_id == created.pet_id
    assert found.state == AdoptionState.in_process


def test_get_adoption_status_not_found(db_session):
    random_uuid = uuid.uuid4()
    result = adoption_status_service.get_adoption_status(db_session, random_uuid)
    assert result is None


def test_update_adoption_status(db_session):
    pet_uuid = uuid.uuid4()
    schema = AdoptionStatusCreate(pet_id=pet_uuid, state=AdoptionState.available)
    adoption_status_service.create_adoption_status(db_session, schema)

    update_schema = AdoptionStatusUpdate(state=AdoptionState.adopted)
    updated = adoption_status_service.update_adoption_status(db_session, pet_uuid, update_schema)

    assert updated is not None
    assert updated.state == AdoptionState.adopted


def test_update_adoption_status_not_found(db_session):
    random_uuid = uuid.uuid4()
    update_schema = AdoptionStatusUpdate(state=AdoptionState.adopted)
    result = adoption_status_service.update_adoption_status(db_session, random_uuid, update_schema)
    assert result is None


def test_delete_adoption_status(db_session):
    pet_uuid = uuid.uuid4()
    schema = AdoptionStatusCreate(pet_id=pet_uuid, state=AdoptionState.available)
    adoption_status_service.create_adoption_status(db_session, schema)

    deleted = adoption_status_service.delete_adoption_status(db_session, pet_uuid)
    assert deleted is True

    result = adoption_status_service.get_adoption_status(db_session, pet_uuid)
    assert result is None


def test_delete_adoption_status_not_found(db_session):
    random_uuid = uuid.uuid4()
    deleted = adoption_status_service.delete_adoption_status(db_session, random_uuid)
    assert deleted is False
