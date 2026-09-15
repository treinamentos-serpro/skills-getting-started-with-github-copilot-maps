from src import app as app_module


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities_with_no_store_cache(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    assert response.json() == app_module.activities


def test_signup_adds_participant_to_activity(client):
    email = "alex@mergington.edu"

    response = client.post("/activities/Basketball Team/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Basketball Team"}
    assert email in app_module.activities["Basketball Team"]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    response = client.post("/activities/Unknown Activity/signup", params={"email": "alex@mergington.edu"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_returns_400_for_duplicate_participant(client):
    existing_email = app_module.activities["Chess Club"]["participants"][0]

    response = client.post("/activities/Chess Club/signup", params={"email": existing_email})

    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_unregister_removes_participant_from_activity(client):
    email = app_module.activities["Programming Class"]["participants"][0]

    response = client.delete("/activities/Programming Class/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from Programming Class"}
    assert email not in app_module.activities["Programming Class"]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    response = client.delete("/activities/Unknown Activity/signup", params={"email": "alex@mergington.edu"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_returns_404_for_missing_participant(client):
    response = client.delete("/activities/Basketball Team/signup", params={"email": "alex@mergington.edu"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Student not signed up for this activity"}