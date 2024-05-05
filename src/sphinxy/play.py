from pathlib import Path
from collections import deque

import streamlit as st
from openai import OpenAI

from ai import LLModel, Interaction
from levels import BasicGame, Level
from utils import check_requirements
from log_config import setup_logger

logger = setup_logger()

# TODO: Move to config
LLM_SERVER_URL: str = "http://localhost:8000/"
MODEL_PATH: Path = Path("models/Meta-Llama-3-8B-Instruct-Q8_0.gguf")

GAME_HEADER = "Welcome adventurer! You just have entered Level 1 of the Sphinxy Game. 🦁"
GAME_DESCRIPTION = """
    Sphinxy is a magical and cute sphinx who is hidding a scret key to the next level.
    Your goal is to convince Sphinxy to reveal the secret key to you by asking questions.
    There are 5 levels in total. Each level is harder the previous one.
    Can you reach the end of the game?
    Good luck! 🍀
"""


def initialize_game():
    """
    Initializes or retrieves variables for the game from session state.
    """
    if "llm_model" not in st.session_state:
        client = OpenAI(api_key="free_models", base_url=LLM_SERVER_URL + "v1")
        st.session_state.llm_model = LLModel(model_path=str(MODEL_PATH), client=client)
        st.session_state.session_memory = deque(maxlen=10)
        st.session_state.game = BasicGame()


def launch_game_loop():
    """Entry point for the game in the terminal version."""
    logger.info("Game started.")
    initialize_game()
    game = st.session_state.game
    current_level: Level = game.get_current_level()

    st.title(f"- Level {current_level.number} -")

    if st.session_state.get("first_run", True):
        st.subheader(GAME_HEADER, anchor=None, help=None, divider=False)
        st.markdown(GAME_DESCRIPTION)
        st.session_state.first_run = False
    else:
        # Start submit layout
        left_side, space_for_button = st.columns([5, 1])

        with left_side:
            user_guess = st.text_input(
                label="Do you know the secret-key?",
                placeholder="Type the secret-key here...",
                key="user_guess",
                label_visibility="collapsed",
            )

        with space_for_button:
            submit_button = st.button(
                "Submit", key="submit_guess", help="Click to submit your guess.", type="primary"
            )

        if submit_button:
            logger.info(f"User guess: {user_guess}")
            if user_guess == "":
                msg = "Oops! It looks like you forgot to type the secret-key. Try again."
                is_correct = False
            else:
                is_correct, msg = current_level.check_answer(user_guess)

            # Make sphinxy answer in the chat
            st.chat_message("Sphinxy", avatar="🦁").markdown(msg)

            if is_correct:
                game.increase_one_level()
                if game.is_game_over():
                    st.success("🎉🎉 Congratulations! You finished the game! 🎉🎉")
                else:
                    current_level = game.get_current_level()
                    congrats_msg = f"""
                        "Welcome to Level {current_level.number} 🔥 This one will be harder 😈"
                    """
                    st.success(congrats_msg)

    # show previous interactions, if any
    for interaction in st.session_state.session_memory:
        avatar = "🦁" if interaction.role == "assistant" else None
        with st.chat_message(interaction.role, avatar=avatar):
            st.markdown(interaction.message)

    # communicate with sphinxy
    if prompt := st.chat_input("Ask Sphinxy a question (:"):
        st.chat_message("user").markdown(prompt)

        with st.chat_message("Spninxy", avatar="🦁"):
            # Call to the AI model
            llm_model: LLModel = st.session_state.llm_model
            stream = llm_model.generate_response(
                prompt, current_level, memory=st.session_state.session_memory
            )
            response = st.write_stream(stream)

        # Save the conversation in the session memory
        st.session_state.session_memory.append(Interaction("user", prompt))
        st.session_state.session_memory.append(Interaction("assistant", response))


if __name__ == "__main__":
    if not st.session_state.get("requirements_checked", False):
        check_requirements(MODEL_PATH, LLM_SERVER_URL)
        st.session_state.requirements_checked = True

    launch_game_loop()
