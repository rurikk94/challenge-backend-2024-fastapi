import random
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_bonus_rules():
    response = client.get("/v1/bonus_rules/")
    assert response.status_code == 200
    return response.json()

def test_get_bonus_rules_random():
    data = test_get_bonus_rules()
    bonus_rule = random.choice(data["data"])
    bonus_rule_id = bonus_rule["bonus_rule_id"]
    response = client.get(f"/v1/bonus_rules/{bonus_rule_id}")
    assert response.status_code == 200

