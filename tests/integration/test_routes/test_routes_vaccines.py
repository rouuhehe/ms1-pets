import pytest
import uuid
import datetime
from fastapi.testclient import TestClient
from fastapi import status, HTTPException
from app.main import app

client = TestClient(app)


@pytest.fixture
def fake_vaccine():
    return {
        "id": str(uuid.uuid4()),
        "pet_id": str(uuid.uuid4()),
        "type": "Rabies",
        "date": str(datetime.date.today())
    }


def test_list_vaccines(monkeypatch, fake_vaccine):
    def mock_get_vaccines(db, pet_id=None, skip=0, limit=20):
        return [fake_vaccine]

    monkeypatch.setattr("app.services.vaccine_service.get_vaccines", mock_get_vaccines)

    response = client.get("/vaccines/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["type"] == "Rabies"


def test_get_vaccine_found(monkeypatch, fake_vaccine):
    def mock_get_vaccine_by_id(db, vaccine_id):
        return fake_vaccine

    monkeypatch.setattr("app.services.vaccine_service.get_vaccine_by_id", mock_get_vaccine_by_id)

    response = client.get(f"/vaccines/{fake_vaccine['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == fake_vaccine["id"]


def test_get_vaccine_not_found(monkeypatch):
    def mock_get_vaccine_by_id(db, vaccine_id):
        raise HTTPException(status_code=404, detail="Vaccine not found")

    monkeypatch.setattr("app.services.vaccine_service.get_vaccine_by_id", mock_get_vaccine_by_id)

    response = client.get(f"/vaccines/{uuid.uuid4()}")
    print(response.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Vaccine not found"


def test_create_vaccine(monkeypatch, fake_vaccine):
    def mock_create_vaccine(db, vaccine):
        return fake_vaccine

    monkeypatch.setattr("app.services.vaccine_service.create_vaccine", mock_create_vaccine)

    payload = {
        "pet_id": fake_vaccine["pet_id"],
        "type": "Rabies",
        "date": fake_vaccine["date"]
    }
    response = client.post("/vaccines/", json=payload)
    assert response.status_code == 201
    assert response.json()["type"] == "Rabies"


def test_update_vaccine(monkeypatch, fake_vaccine):
    def mock_update_vaccine(db, vaccine_id, vaccine_update):
        return {**fake_vaccine, "type": "Distemper"}

    monkeypatch.setattr("app.services.vaccine_service.update_vaccine", mock_update_vaccine)

    payload = {"type": "Distemper"}
    response = client.patch(f"/vaccines/{fake_vaccine['id']}", json=payload)
    assert response.status_code == 200
    assert response.json()["type"] == "Distemper"


def test_update_vaccine_not_found(monkeypatch):
    def mock_update_vaccine(db, vaccine_id, vaccine_update):
        raise HTTPException(status_code=404, detail="Vaccine not found")

    monkeypatch.setattr("app.services.vaccine_service.update_vaccine", mock_update_vaccine)

    payload = {"type": "Distemper"}
    response = client.patch(f"/vaccines/{uuid.uuid4()}", json=payload)
    print(response.json())

    assert response.status_code == 404
    assert response.json()["detail"] == "Vaccine not found"


def test_delete_vaccine_success(monkeypatch):
    def mock_delete_vaccine(db, vaccine_id):
        return True

    monkeypatch.setattr("app.services.vaccine_service.delete_vaccine", mock_delete_vaccine)

    response = client.delete(f"/vaccines/{uuid.uuid4()}")
    assert response.status_code == 204
    assert response.text == ""


def test_delete_vaccine_not_found(monkeypatch):
    def mock_delete_vaccine(db, vaccine_id):
        raise HTTPException(status_code=404, detail="Vaccine not found")

    monkeypatch.setattr("app.services.vaccine_service.delete_vaccine", mock_delete_vaccine)

    response = client.delete(f"/vaccines/{uuid.uuid4()}")
    print(response.json())

    assert response.status_code == 404
    assert response.json()["detail"] == "Vaccine not found"
