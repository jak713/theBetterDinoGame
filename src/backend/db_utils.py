import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "db", "dino_game.db")

class DatabaseManager:
    def __init__(self):
        self.db_path = DB_PATH

    def connect_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def insert_player_db(self, username: str) -> int:
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO players (username) VALUES (?)", (username,))
        db.commit()
        player_id = cursor.lastrowid
        cursor.close()
        db.close()
        return player_id

    def insert_game_run_db(self, player_id: int) -> int:
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO game_runs (player_id) VALUES (?)", (player_id,))
        db.commit()
        game_run_id = cursor.lastrowid
        cursor.close()
        db.close()
        return game_run_id

    def update_game_run_db(self, game_run_id: int, score: int) -> bool:
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE game_runs SET score = ?, ended_at = CURRENT_TIMESTAMP "
            "WHERE id = ?",
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
        cursor.execute("DELETE FROM game_runs WHERE id = ?", (game_run_id,))
        db.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        db.close()
        return rows_affected > 0
