import json
from dataclasses import dataclass
from .gamestate import GameState
from .constants import LOCAL_SCORES


@dataclass
class GameRun:
    """
    Class to keep track of each game run info. 
    """
    player_id: int
    game_run_id: int
    username: str
    score: float=0.0
    state: GameState = GameState.TITLE

    def update_score(self, dt: float, multiplier: int) -> None:
        if self.is_active():
            self.score += dt * multiplier

    def transition(self, new_state: GameState) -> None:
        self.state = new_state

    def is_active(self) -> bool:
        return self.state == GameState.NEWGAME

    def final_score(self) -> int:
        """Returns integer score."""
        return int(self.score)
    
    def save_to_file(self):
        """Saves current run username + score into a local json file"""
        try:
            with open(LOCAL_SCORES, 'r') as f:
                scores = json.load(f)
        except json.JSONDecodeError:
            # JSON decode error happens when there is something wrong with the json data, we can overwrite
            print("Local score data may be corrupted, overwriting.")
            scores = []
        except FileNotFoundError:
            # local file does not exist yet so this will be our first score
            scores = []

        # add current data to scores
        scores.append({"username": self.username, "score": int(self.score)})
        # make sure subdir .local_scores exists, or make it if needed
        LOCAL_SCORES.parent.mkdir(exist_ok=True, parents=True)

        with open(LOCAL_SCORES, 'w') as f:
            json.dump(scores, f)
