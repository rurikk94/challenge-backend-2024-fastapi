import random
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_combination_rules():
    response = client.get("/v1/combination_rules/")
    assert response.status_code == 200
    return response.json()

def test_get_combination_rules_random():
    data = test_get_combination_rules()
    combination_rule = random.choice(data["data"])
    combination_rule_id = combination_rule["combination_rule_id"]
    response = client.get(f"/v1/combination_rules/{combination_rule_id}")
    assert response.status_code == 200