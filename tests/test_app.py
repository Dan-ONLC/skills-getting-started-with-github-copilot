import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a FastAPI TestClient for each test."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities state before each test."""
    original_state = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_state)


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Swimming Club",
        "Art Club",
        "Drama Society",
        "Debate Team",
        "Robotics Club",
    ]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    for activity in expected_activities:
        assert activity in data


def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Swimming Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email.lower() in activities[activity_name]["participants"]


def test_duplicate_signup_returns_409(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    original_count = len(activities[activity_name]["participants"])

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 409
    assert "already signed up" in response.json()["detail"]
    assert len(activities[activity_name]["participants"]) == original_count


def test_delete_existing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email.lower() not in activities[activity_name]["participants"]


def test_delete_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "nonexistent@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert "not signed up" in response.json()["detail"]
