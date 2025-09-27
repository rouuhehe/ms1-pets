import datetime
import uuid
from app.models.adoption_status import AdoptionStatus, AdoptionState


def test_default_adoption_status():
    pet_uuid = uuid.uuid4()
    status = AdoptionStatus(pet_id=pet_uuid)

    assert status.pet_id == pet_uuid
    assert status.state == AdoptionState.available
    assert isinstance(status.last_updated, datetime.datetime)


def test_repr_contains_fields():
    pet_uuid = uuid.uuid4()
    status = AdoptionStatus(pet_id=pet_uuid, state=AdoptionState.in_process)
    text = repr(status)

    assert f"pet_id={pet_uuid}" in text
    assert "state=in_process" in text
    assert "last_updated=" in text
