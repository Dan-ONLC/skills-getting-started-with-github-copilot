"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },

    # Sports activities
    "Soccer Team": {
        "description": "Competitive soccer team practices and matches",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["sarah@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Lap swimming, technique drills, and friendly meets",
        "schedule": "Tuesdays and Thursdays, 5:00 PM - 6:30 PM",
        "max_participants": 18,
        "participants": []
    },

    # Artistic activities
    "Art Club": {
        "description": "Explore painting, drawing, and mixed media projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["liz@mergington.edu"]
    },
    "Drama Society": {
        "description": "Theatre rehearsals, workshops, and seasonal productions",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": []
    },

    # Intellectual activities
    "Debate Team": {
        "description": "Practice argumentation, public speaking, and competitions",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["michael@mergington.edu"]
    },
    "Robotics Club": {
        "description": "Build and program robots; prepare for competitions",
        "schedule": "Tuesdays, 4:00 PM - 6:00 PM",
        "max_participants": 12,
        "participants": ["daniel@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Normalize email and prevent duplicate signups (case-insensitive)
    normalized_email = email.strip().lower()
    existing = [p.strip().lower() for p in activity.get("participants", [])]
    if normalized_email in existing:
        raise HTTPException(status_code=409,
                            detail=f"{email} is already signed up for {activity_name}")

    # Add student
    activity["participants"].append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def remove_participant(activity_name: str, email: str):
    """Remove a participant from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    normalized_email = email.strip().lower()
    # Find and remove any matching participant (case-insensitive)
    for p in list(activity.get("participants", [])):
        if p.strip().lower() == normalized_email:
            activity["participants"].remove(p)
            return {"message": f"Removed {normalized_email} from {activity_name}"}

    raise HTTPException(status_code=404,
                        detail=f"{email} is not signed up for {activity_name}")
