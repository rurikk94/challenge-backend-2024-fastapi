import random
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_interpretation_rules():
    response = client.get("/v1/interpretation_rules/")
    assert response.status_code == 200
    return response.json()

def test_get_interpretation_rules_random():
    data = test_get_interpretation_rules()
    interpretation_rule = random.choice(data["data"])
    interpretation_rule_id = interpretation_rule["interpretation_rule_id"]
    response = client.get(f"/v1/interpretation_rules/{interpretation_rule_id}")
    assert response.status_code == 200