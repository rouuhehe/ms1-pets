import uuid
import datetime
from sqlalchemy.orm import Session
from app.models.adoption_center import AdoptionCenter
from app.models.pet import Pet
from app.services import vaccine_service
from app.schemas import VaccineCreate, VaccineUpdate


def make_center_and_pet(db: Session):
    center = AdoptionCenter(name="Centro Test", address="Dir", city="City")
    db.add(center)
    db.commit()
    db.refresh(center)

    birth_date = datetime.date.today().replace(year=datetime.date.today().year - 2)
    pet = Pet(
        name="TestPet",
        species="Dog",
        breed="Mix",
        birth_date=birth_date,
        adoption_center_id=center.id,
    )
    db.add(pet)
    db.commit()
    db.refresh(pet)
    return center, pet


def test_create_and_get_vaccine(db_session: Session):
    _, pet = make_center_and_pet(db_session)

    payload = VaccineCreate(
        pet_id=pet.id,
        type="Rabies",
        date=datetime.date.today()
    )
    created = vaccine_service.create_vaccine(db_session, payload)

    assert created.id is not None
    assert isinstance(created.id, uuid.UUID)
    assert created.pet_id == pet.id
    assert created.type == "Rabies"

    fetched = vaccine_service.get_vaccine_by_id(db_session, created.id)
    assert fetched is not None
    assert fetched.id == created.id


def test_get_vaccines_filter_and_pagination(db_session: Session):
    _, pet1 = make_center_and_pet(db_session)
    _, pet2 = make_center_and_pet(db_session)

    for i in range(4):
        vaccine_service.create_vaccine(
            db_session,
            VaccineCreate(pet_id=pet1.id, type=f"V{i}", date=datetime.date.today())
        )

    vaccine_service.create_vaccine(
        db_session,
        VaccineCreate(pet_id=pet2.id, type="Other", date=datetime.date.today())
    )

    all_vaccines = vaccine_service.get_vaccines(db_session)
    assert len(all_vaccines) >= 5

    pet1_vaccines = vaccine_service.get_vaccines(db_session, pet_id=pet1.id)
    assert all(v.pet_id == pet1.id for v in pet1_vaccines)

    page1 = vaccine_service.get_vaccines(db_session, skip=0, limit=2)
    page2 = vaccine_service.get_vaccines(db_session, skip=2, limit=2)
    assert len(page1) == 2
    assert len(page2) == 2


def test_update_and_delete_vaccine(db_session: Session):
    _, pet = make_center_and_pet(db_session)
    created = vaccine_service.create_vaccine(
        db_session,
        VaccineCreate(pet_id=pet.id, type="Rabies", date=datetime.date.today())
    )

    updated = vaccine_service.update_vaccine(
        db_session, created.id, VaccineUpdate(type="Distemper")
    )
    assert updated is not None
    assert updated.type == "Distemper"

    ok = vaccine_service.delete_vaccine(db_session, created.id)
    assert ok is True
    assert vaccine_service.get_vaccine_by_id(db_session, created.id) is None


def test_update_delete_not_found(db_session: Session):
    fake_id = uuid.uuid4()
    assert vaccine_service.get_vaccine_by_id(db_session, fake_id) is None
    assert vaccine_service.update_vaccine(db_session, fake_id, VaccineUpdate(type="X")) is None
    assert vaccine_service.delete_vaccine(db_session, fake_id) is False
