from fastapi.testclient import TestClient
from src.app import app
import urllib.parse

client = TestClient(app)


def test_get_activities():
    # Arrange
    # client is ready

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data


def test_signup_duplicate_and_remove_flow():
    # Arrange
    activity = "Chess Club"
    email = "pytest_user@example.com"
    quoted_activity = urllib.parse.quote(activity, safe="")
    quoted_email = urllib.parse.quote(email, safe="")

    # Ensure clean start: remove if present (ignore 404)
    client.delete(f"/activities/{quoted_activity}/participants?email={quoted_email}")

    # Act: sign up
    signup_resp = client.post(f"/activities/{quoted_activity}/signup?email={quoted_email}")

    # Assert signup succeeded and participant appears
    assert signup_resp.status_code == 200
    participants = client.get("/activities").json()[activity]["participants"]
    assert email in participants

    # Act: attempt duplicate signup
    dup_resp = client.post(f"/activities/{quoted_activity}/signup?email={quoted_email}")

    # Assert duplicate rejected
    assert dup_resp.status_code == 400

    # Act: remove participant
    remove_resp = client.delete(f"/activities/{quoted_activity}/participants?email={quoted_email}")

    # Assert removal succeeded and participant is gone
    assert remove_resp.status_code == 200
    participants_after = client.get("/activities").json()[activity]["participants"]
    assert email not in participants_after


def test_remove_nonexistent():
    # Arrange
    activity = "Chess Club"
    email = "noone@example.com"
    quoted_activity = urllib.parse.quote(activity, safe="")
    quoted_email = urllib.parse.quote(email, safe="")

    # Act
    response = client.delete(f"/activities/{quoted_activity}/participants?email={quoted_email}")

    # Assert
    assert response.status_code == 404
