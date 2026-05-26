from fastapi.testclient import TestClient
from src.app import app
import urllib.parse

client = TestClient(app)


def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert "Chess Club" in data


def test_signup_duplicate_and_remove_flow():
    activity = "Chess Club"
    email = "pytest_user@example.com"
    quoted_activity = urllib.parse.quote(activity, safe="")
    quoted_email = urllib.parse.quote(email, safe="")

    # Ensure clean start: remove if present (ignore 404)
    client.delete(f"/activities/{quoted_activity}/participants?email={quoted_email}")

    # Sign up
    r = client.post(f"/activities/{quoted_activity}/signup?email={quoted_email}")
    assert r.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

    # Duplicate signup should fail
    r2 = client.post(f"/activities/{quoted_activity}/signup?email={quoted_email}")
    assert r2.status_code == 400

    # Remove participant
    r3 = client.delete(f"/activities/{quoted_activity}/participants?email={quoted_email}")
    assert r3.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_remove_nonexistent():
    activity = "Chess Club"
    email = "noone@example.com"
    quoted_activity = urllib.parse.quote(activity, safe="")
    quoted_email = urllib.parse.quote(email, safe="")

    r = client.delete(f"/activities/{quoted_activity}/participants?email={quoted_email}")
    assert r.status_code == 404
