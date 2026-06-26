import mysql.connector
from .config import db_config


class DatabaseManager:
    def __init__(self):
        self.db_config = db_config

    def connect_db(self):
        return mysql.connector.connect(**self.db_config)

    def insert_player_db(self, username: str) -> int:
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO players (username) VALUES (%s)", (username,))
        db.commit()
        player_id = cursor.lastrowid
        cursor.close()
        db.close()
        return player_id

    def insert_game_run_db(self, player_id: int) -> int:
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO game_runs (player_id) VALUES (%s)", (player_id,))
        db.commit()
        game_run_id = cursor.lastrowid
        cursor.close()
        db.close()
        return game_run_id

    def update_game_run_db(self, game_run_id: int, score: int) -> bool:
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE game_runs SET score = %s, ended_at = CURRENT_TIMESTAMP "
            "WHERE id = %s",
            (score, game_run_id),
        )
        db.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        db.close()
        return rows_affected > 0

    def fetch_leaderboard_db(self) -> list:
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT username, score FROM game_runs "
            "JOIN players ON game_runs.player_id = players.id "
            "ORDER BY score DESC LIMIT 10"
        )
        results = cursor.fetchall()
        cursor.close()
        db.close()
        return results

    def delete_game_run_db(self, game_run_id: int) -> bool:
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM game_runs WHERE id = %s", (game_run_id,))
        db.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        db.close()
        return rows_affected > 0
