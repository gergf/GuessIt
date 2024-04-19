from typing import Optional

from dataclasses import dataclass


@dataclass
class Level:
    """
    Represents a level in the game.
    """

    number: int
    answer: str
    prompt: Optional[str] = None
    postprocessing: Optional[str] = None

    def __str__(self):
        return f"Level {self.number}"


# Implement the levels of the game
LEVEL_ONE = Level(1, "nice")
LEVEL_TWO = Level(2, "veronica")
LEVELS = [LEVEL_ONE, LEVEL_TWO]
