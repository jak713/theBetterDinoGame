import pytest
from api import app
import api


@pytest.fixture
def client():
    """
    Based on https://flask.palletsprojects.com/en/stable/testing/, 
    the app exists in the API file so we import it directly as opposed to 
    importing a create_app function
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

class TestAPI:
    def test_create_player_success(self, client, monkeypatch):
        monkeypatch.setattr(api.db, "insert_player_db", lambda id: 99)

        response = client.post("/players", json={"username": "test"})

        assert response.status_code == 201
        assert response.get_json() == {"message": "Player created", "player_id": 99}


    def test_create_player_missing_username_returns_error(self, client):
        response = client.post("/players", json={})

        assert response.status_code == 400
        assert response.get_json() == {"error": "Missing username"}


    def test_create_player_empty_username_returns_error(self, client):
        response = client.post("/players", json={"username": ""})

        assert response.status_code == 400
        assert response.get_json() == {"error": "Username cannot be empty"}


    def test_create_game_run_success(self, client, monkeypatch):
        monkeypatch.setattr(api.db, "insert_game_run_db", lambda id: 1)
        response = client.post("/game_runs", json={"player_id":99})

        assert response.status_code == 201
        assert response.get_json() == {"message": "Game run created", "game_run_id": 1}


    def test_update_game_run_wo_score_returns_error(self, client):
        response = client.put("/game_runs/0", json={})
        
        assert response.status_code == 400

    def test_leaderboard_success(self, client, monkeypatch):
        monkeypatch.setattr(api.db, "fetch_leaderboard_db", lambda: [])
        
        response = client.get("/leaderboard")

        assert response.status_code == 200


    def test_delete_game_run_success(self, client, monkeypatch):
        monkeypatch.setattr(api.db, "delete_game_run_db", lambda id: True)

        response = client.delete("/game_runs/0")

        assert response.status_code == 200
        assert response.get_json() == {"message": "Game run deleted"}


    def test_delete_game_run_not_found_returns_error(self, client, monkeypatch):
        monkeypatch.setattr(api.db, "delete_game_run_db", lambda id: False)

        response = client.delete("/game_runs/0")

        assert response.status_code == 404
        assert response.get_json() == {"error": "Game run not found"}
