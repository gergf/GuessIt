import logging

from ai import Sphinxy
from levels import LEVELS

logging.basicConfig(
    filename="game.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

INTRO_MESSAGE = """
############################################
Welcome to the game!

The goal is simple: there is a magic word you need to guess in order to complete each level.

To obtain information, you will be able to interact with Sphinxy.

Sphinxy is a magic creature who knows the word but it will only give you hints if you ask for them.
She will hide the magic word from you, so you will need to trick her into revealing it.

Each time you guess sucessfully, you will be able to move to the next level.
Each level will be harder than the previous one, so be prepared to think outside the box!

Let's get started. Good luck!
############################################
"""
INSTRUCTIONS = "Type [Q] to ask a question. [A] to make a guess. [EXIT] to exit the game."


def main():
    """
    Entry point for the game in the terminal version.
    """
    logger.info("Starting game...")
    print(INTRO_MESSAGE)

    print("Sphinxy: Can you guess the magic word?")
    print(INSTRUCTIONS)

    # Start the game
    n_levels = len(LEVELS)
    current_level = 0
    PLAY_GAME = True
    while (current_level < n_levels) and (PLAY_GAME is True):
        level = LEVELS[current_level]
        print("------------------------------------")
        print(f"Level {level.number}")

        LEVEL_COMPLETED = False
        while not LEVEL_COMPLETED:
            # Get the user input
            user_input = input("What do you want to do? [A/Q/EXIT]: ").lower()
            if user_input == "q":
                user_question = input("What is your question? ").lower()
                q_answer = Sphinxy.answer_question(
                    user_question, level.prompt, level.postprocessing
                )
                print(f"Sphinxy: {q_answer}")
            elif user_input == "a":
                user_guess = input("What is the magic word? ").lower()
                if user_guess == level.answer:
                    print(f"Congratulations! {level.answer} was the magic word!")
                    LEVEL_COMPLETED = True
            elif user_input == "exit":
                print("Sphinxy: I'm sorry to see you leaving -- take care and see you soon!")
                PLAY_GAME = False
                break
            else:
                print("Invalid input. Please try again.")
                continue

        # Increase level of difficulty
        current_level += 1

    if current_level == n_levels:
        print("------------------------------------")
        print("Congratulations! You have completed the game.")
        logger.info("Game completed successfully.")


if __name__ == "__main__":
    main()
