import requests

API_URL = "http://127.0.0.1:5000"


# Create - POST
def create_player_api_client(username: str):
    create_player = {"username": username}
    response = requests.post(f"{API_URL}/players", json=create_player)
    return response.json()


def create_game_run_api_client(player_id: int):
    create_game_run = {"player_id": player_id}
    response = requests.post(f"{API_URL}/game_runs", json=create_game_run)
    return response.json()


# Read - GET
def fetch_leaderboard_api_client():
    response = requests.get(f"{API_URL}/leaderboard")
    return response.json()


# Update - PUT
def update_game_run_api_client(game_run_id: int, score: int):
    updated_data = {"score": score}
    response = requests.put(f"{API_URL}/game_runs/{game_run_id}", json=updated_data)
    return response.json()


# Delete - DELETE
def delete_game_run_api_client(game_run_id: int):
    response = requests.delete(f"{API_URL}/game_runs/{game_run_id}")
    return response.json()
