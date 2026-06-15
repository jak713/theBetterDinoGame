import requests

API_URL = "http://127.0.0.1:5000"


def fetch_leaderboard():
    res = requests.get(f"{API_URL}/leaderboard")
    return res.json()
