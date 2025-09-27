import uuid
from app.services import adoption_center_service
from app.schemas import AdoptionCenterCreate, AdoptionCenterUpdate


def test_create_center(db_session):
    schema = AdoptionCenterCreate(
        name="Refugio Patitas",
        address="Av. Siempre Viva 123",
        city="Springfield"
    )
    center = adoption_center_service.create_center(db_session, schema)
    assert center.id is not None
    assert center.name == "Refugio Patitas"
    assert center.address == "Av. Siempre Viva 123"
    assert center.city == "Springfield"


def test_get_center_by_id(db_session):
    schema = AdoptionCenterCreate(name="Refugio Único", address="Calle 2", city="Quito")
    center = adoption_center_service.create_center(db_session, schema)

    found = adoption_center_service.get_center_by_id(db_session, center.id)
    assert found is not None
    assert found.id == center.id
    assert found.name == "Refugio Único"


def test_get_center_by_id_not_found(db_session):
    fake_id = uuid.uuid4()
    found = adoption_center_service.get_center_by_id(db_session, fake_id)
    assert found is None


def test_get_centers(db_session):
    schema1 = AdoptionCenterCreate(name="Refugio A", address="Dir A", city="Ciudad A")
    schema2 = AdoptionCenterCreate(name="Refugio B", address="Dir B", city="Ciudad B")

    adoption_center_service.create_center(db_session, schema1)
    adoption_center_service.create_center(db_session, schema2)

    centers = adoption_center_service.get_centers(db_session)
    assert len(centers) >= 2
    names = [c.name for c in centers]
    assert "Refugio A" in names
    assert "Refugio B" in names


def test_update_center(db_session):
    schema = AdoptionCenterCreate(name="Refugio Inicial", address="Calle 1", city="Lima")
    center = adoption_center_service.create_center(db_session, schema)

    update_schema = AdoptionCenterUpdate(name="Refugio Renovado")
    updated = adoption_center_service.update_center(db_session, center.id, update_schema)
    assert updated.name == "Refugio Renovado"


def test_update_center_not_found(db_session):
    fake_id = uuid.uuid4()
    update_schema = AdoptionCenterUpdate(name="No Existe")
    updated = adoption_center_service.update_center(db_session, fake_id, update_schema)
    assert updated is None


def test_delete_center(db_session):
    schema = AdoptionCenterCreate(name="Refugio Temporal", address="Calle Falsa", city="Bogotá")
    center = adoption_center_service.create_center(db_session, schema)

    result = adoption_center_service.delete_center(db_session, center.id)
    assert result is True

    found = adoption_center_service.get_center_by_id(db_session, center.id)
    assert found is None


def test_delete_center_not_found(db_session):
    fake_id = uuid.uuid4()
    result = adoption_center_service.delete_center(db_session, fake_id)
    assert result is False
