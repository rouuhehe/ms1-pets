import datetime
import uuid
from app.models.pet import Pet


def test_pet_repr_and_age_category():
    birth_date = datetime.date.today().replace(year=datetime.date.today().year - 3)
    pet = Pet(
        name="Buddy",
        species="Dog",
        breed="Bulldog",
        birth_date=birth_date,
        adoption_center_id=uuid.uuid4(),
    )

    assert "years" in pet.age
    assert pet.age_category == "adult"

    text = repr(pet)
    assert "Buddy" in text
    assert "Dog" in text
    assert "Bulldog" in text
