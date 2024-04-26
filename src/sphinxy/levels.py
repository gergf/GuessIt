from typing import Optional, Tuple

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

    def check_answer(self, user_answer: str) -> Tuple[bool, str]:
        is_correct = user_answer.lower() == self.answer.lower()
        if is_correct:
            msg = f"Congratulations, you found the key to Level {self.number}. 🎉"
        else:
            msg = f"Sorry, '{user_answer}' is not the key. Try again. 🤔"
        return is_correct, msg


class Game:
    """
    A game is a sequence of levels.
    """

    def __init__(self, levels: list[Level]) -> None:
        self.levels = levels
        self.n_levels = len(levels)
        self.current_level = 0

    def __str__(self):
        return f"Game with {len(self.levels)} levels"

    def get_current_level(self) -> Level:
        if self.current_level >= self.n_levels:
            raise ValueError("No more levels available")
        return self.levels[self.current_level]

    def increase_one_level(self) -> Level:
        self.current_level += 1

    def is_game_over(self) -> bool:
        return self.current_level >= self.n_levels


class BasicGame(Game):
    """
    A basic game with three levels.
    """

    LEVELS = [
        Level(1, "paella"),
        Level(2, "rocket"),
        Level(3, "frankenstein"),
    ]

    def __init__(self) -> None:
        super().__init__(self.LEVELS)