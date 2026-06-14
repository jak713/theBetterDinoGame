from flask import Flask, jsonify, request
from db_utils import DatabaseManager

app = Flask(__name__)

db = DatabaseManager()

@app.route("/players", methods=["POST"])
def create_player():
    pass

@app.route("/game_runs", methods=["POST"])
def create_game_run():
    pass

@app.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    pass

@app.route("/player_runs/<int:game_run_id>")
def delete_game_run(game_run_id):
    pass


if __name__ == "__main__":
    app.run(debug=True)

