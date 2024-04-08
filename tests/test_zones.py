import random
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_zones():
    response = client.get("/v1/zones/")
    assert response.status_code == 200
    return response.json()

def test_zones_random():
    data = test_zones()
    zone = random.choice(data["data"])
    zone_id = zone["zone_id"]
    response = client.get(f"/v1/zones/{zone_id}")
    assert response.status_code == 200


