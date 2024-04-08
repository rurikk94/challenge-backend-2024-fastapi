import random
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_paycodes_distribution():
    response = client.get("/v1/paycodes_distributions/")
    assert response.status_code == 200
    return response.json()

def test_get_paycodes_distribution_random():
    data = test_get_paycodes_distribution()
    paycode = random.choice(data["data"])
    paycodes_distibution_id = paycode["paycodes_distibution_id"]
    response = client.get(f"/v1/paycodes_distributions/{paycodes_distibution_id}")
    assert response.status_code == 200