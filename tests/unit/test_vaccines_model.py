import datetime
from app.models.vaccine import Vaccine


def test_vaccine_repr():
    v = Vaccine(
        pet_id=10,
        type="Rabies",
        date=datetime.date.today(),
    )

    text = repr(v)
    assert "pet_id=10" in text
    assert "Rabies" in text
    assert "date=" in text
