import pytest
from game.dinogame import clean_username 

class TestUtils:
    def test_clean_username_returns_player1(self):
        assert clean_username("") == "player1"
        assert clean_username("   ") == "player1"

    def test_clean_username_returns_stripped(self):
        assert clean_username("  test") == "test"
