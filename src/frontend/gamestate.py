from enum import Enum


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    LEADERBOARD = 2
    DELETE_RUN = 3
