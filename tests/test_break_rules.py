import random
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_break_rules():
    response = client.get("/v1/break_rules/")
    assert response.status_code == 200
    return response.json()

def test_get_break_rules_random():
    data = test_get_break_rules()
    break_rule = random.choice(data["data"])
    break_rule_id = break_rule["break_rule_id"]
    response = client.get(f"/v1/break_rules/{break_rule_id}")
    assert response.status_code == 200