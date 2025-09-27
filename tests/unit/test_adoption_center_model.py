from app.models.adoption_center import AdoptionCenter


def test_create_adoption_center():
    center = AdoptionCenter(
        name="Happy Paws",
        address="123 Street",
        city="Dogtown",
        lat=10.123,
        lon=-20.456,
    )
    assert center.name == "Happy Paws"
    assert center.city == "Dogtown"
    assert isinstance(center.pets, list)
