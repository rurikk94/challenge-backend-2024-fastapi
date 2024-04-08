import random
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_holidays():
    response = client.get("/v1/holidays/")
    assert response.status_code == 200
    return response.json()

def test_get_holidays_random():
    data = test_get_holidays()
    holiday = random.choice(data["data"])
    holiday_id = holiday["holiday_id"]
    response = client.get(f"/v1/holidays/{holiday_id}")
    assert response.status_code == 200