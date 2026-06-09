import mysql.connector
from config import db_config

class DatabaseManager:

    # constructor stores db_config for each db object created
    def __init__(self):
        self.db_config = db_config

    def connect_db(self):
        return mysql.connector.connect(**self.db_config)

    def insert_player(self):
        pass

    def insert_player_run(self):
        pass

    def fetch_leaderboard(self):
        pass

    def delete_player_run(self):
        pass


