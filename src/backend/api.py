from flask import Flask, jsonify, request
from .db_utils import DatabaseManager

app = Flask(__name__)

db = DatabaseManager()


@app.route("/players", methods=["POST"])
def create_player_api():
    data = request.get_json()

    if not data or "username" not in data:
        return jsonify({"error": "Missing username"}), 400

    username = data["username"].strip()

    if not username:
        return jsonify({"error": "Username cannot be empty"}), 400

    player_id = db.insert_player_db(username)

    if player_id:
        return jsonify({"message": "Player created", "player_id": player_id}), 201

    return jsonify({"error": "Player not created"}), 500


# Function created at the start of the game run. started_at time logged in database.
@app.route("/game_runs", methods=["POST"])
def create_game_run_api():
    data = request.get_json()

    if not data or "player_id" not in data:
        return jsonify({"error": "Missing player_id"}), 400

    game_run_id = db.insert_game_run_db(data["player_id"])

    if game_run_id:
        return jsonify({"message": "Game run created", "game_run_id": game_run_id}), 201

    return jsonify({"error": "Game run not created"}), 500


# Function updates the game run with the player's score and logs ended_at.
@app.route("/game_runs/<int:game_run_id>", methods=["PUT"])
def update_game_run_api(game_run_id):
    data = request.get_json()

    if not data or "score" not in data:
        return jsonify({"error": "Missing score"}), 400

    update_run = db.update_game_run_db(game_run_id, data["score"])

    if update_run:
        return jsonify({"message": "Game run updated"}), 200

    return jsonify({"error": "Game run not updated"}), 404


@app.route("/leaderboard", methods=["GET"])
def get_leaderboard_api():
    leaderboard = db.fetch_leaderboard_db()

    if leaderboard is not None:
        return jsonify(leaderboard), 200

    return jsonify({"error": "Unable to fetch leaderboard"}), 500


@app.route("/game_runs/<int:game_run_id>", methods=["DELETE"])
def delete_game_run_api(game_run_id):
    delete_row = db.delete_game_run_db(game_run_id)

    if delete_row:
        return jsonify({"message": "Game run deleted"}), 200

    return jsonify({"error": "Game run not found"}), 404

def main() -> None:
    app.run(debug=True)

if __name__ == "__main__":
    main()
