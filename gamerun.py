from dataclasses import dataclass
from gamestate import GameState


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

    def finalise(self) -> int:
        """Returns integer score."""
        return int(self.score)

