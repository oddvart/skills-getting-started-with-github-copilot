from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    original_participants = activities[activity_name]["participants"][:]

    try:
        signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert signup_response.status_code == 200
        assert email in activities[activity_name]["participants"]

        remove_response = client.delete(f"/activities/{activity_name}/participants/{email}")
        assert remove_response.status_code == 200
        assert email not in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants


def test_signup_rejects_when_activity_is_full():
    activity_name = "Chess Club"
    email = "full@mergington.edu"
    original_participants = activities[activity_name]["participants"][:]
    original_max = activities[activity_name]["max_participants"]

    try:
        activities[activity_name]["participants"] = ["existing@mergington.edu"] * original_max
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        assert response.status_code == 400
        assert response.json()["detail"] == "Activity is full"
    finally:
        activities[activity_name]["participants"] = original_participants
        activities[activity_name]["max_participants"] = original_max
