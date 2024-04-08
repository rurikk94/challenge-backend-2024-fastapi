import random
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_paycodes_combination():
    response = client.get("/v1/paycodes_combinations/")
    assert response.status_code == 200
    return response.json()

def test_get_paycodes_combination_random():
    data = test_get_paycodes_combination()
    paycodes_combination = random.choice(data["data"])
    paycode_combination_id = paycodes_combination["paycode_combination_id"]
    response = client.get(f"/v1/paycodes_combinations/{paycode_combination_id}")
    assert response.status_code == 200