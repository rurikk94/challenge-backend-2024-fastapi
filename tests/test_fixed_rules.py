import random
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_fixed_rules():
    response = client.get("/v1/fixed_rules/")
    assert response.status_code == 200
    return response.json()

def test_get_fixed_rules_random():
    data = test_get_fixed_rules()
    fixed_rule = random.choice(data["data"])
    fixed_rule_id = fixed_rule["fixed_rule_id"]
    response = client.get(f"/v1/fixed_rules/{fixed_rule_id}")
    assert response.status_code == 200