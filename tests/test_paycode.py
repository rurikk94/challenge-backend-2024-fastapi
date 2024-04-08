import random
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_paycodes():
    response = client.get("/v1/paycodes/")
    assert response.status_code == 200
    return response.json()

def test_get_paycodes_random():
    data = test_get_paycodes()
    paycode = random.choice(data["data"])
    paycode_id = paycode["paycode_id"]
    response = client.get(f"/v1/paycodes/{paycode_id}")
    assert response.status_code == 200