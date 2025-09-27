def test_list_centers_empty(client):
    response = client.get("/centers/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_and_get_center(client):
    payload = {"name": "Refugio Patitas", "address": "Av. Siempre Viva 123", "city": "Springfield"}
    response = client.post("/centers/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Refugio Patitas"

    center_id = data["id"]
    response = client.get(f"/centers/{center_id}")
    assert response.status_code == 200
    assert response.json()["id"] == center_id
