"""Tests for any game logic/adjacent. This will not cover any rendering/display functions"""

import pytest
from dinogame import clean_username 
from gamerun import GameRun
from constants import SCORE_MULTIPLIER
from gamestate import GameState

@pytest.fixture
def run():
    return GameRun(player_id=1, game_run_id=1, username="player1")

class TestCleanUsername:
    def test_clean_username_returns_player1(self):
        assert clean_username("") == "player1"
        assert clean_username("   ") == "player1"

    def test_clean_username_returns_stripped(self):
        assert clean_username("  test") == "test"

class TestGameRun:
    def test_score_starts_as_zero(self, run):
        assert run.score == 0.0

    def test_score_does_not_increase_when_not_active(self, run):
        run.update_score(0.01, SCORE_MULTIPLIER)
        assert run.score == 0.0

    def test_transition_changes_state(self, run):
        run.transition(GameState.NEWGAME)
        assert run.is_active()

    def test_zero_dt_keeps_score_same(self, run):
        run.update_score(0.0, SCORE_MULTIPLIER)
        assert run.score == 0.0

    def test_score_increases(self, run):
        run.transition(GameState.NEWGAME)
        run.update_score(0.1,SCORE_MULTIPLIER)
        assert run.final_score() > 0

