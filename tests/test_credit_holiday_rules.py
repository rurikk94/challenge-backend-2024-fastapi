import random
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_credit_holiday_rules():
    response = client.get("/v1/credit_holiday_rules/")
    assert response.status_code == 200
    return response.json()

def test_credit_holiday_rules_random():
    data = test_credit_holiday_rules()
    credit_holiday_rule = random.choice(data["data"])
    holiday_rule_id = credit_holiday_rule["holiday_rule_id"]
    response = client.get(f"/v1/credit_holiday_rules/{holiday_rule_id}")
    assert response.status_code == 200

