import random
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_pay_rules():
    response = client.get("/v1/pay_rules/")
    assert response.status_code == 200
    return response.json()

def test_get_pay_rules_random():
    data = test_get_pay_rules()
    pay_rule = random.choice(data["data"])
    pay_rule_id = pay_rule["pay_rule_id"]
    response = client.get(f"/v1/pay_rules/{pay_rule_id}")
    assert response.status_code == 200