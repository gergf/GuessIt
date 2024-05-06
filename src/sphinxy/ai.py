from typing import List, Dict
from collections import deque

from openai import OpenAI
from dataclasses import dataclass

from levels import Level
from log_config import setup_logger

logger = setup_logger()


@dataclass
class Interaction:
    """
    Represents an interaction in the game.
    Used to store the role and message of every interaction and store it in the session memory.
    """

    role: str
    message: str

    def __post_init__(self):
        VALID_OPENAI_ROLES = ["user", "assistant", "system"]
        if self.role not in VALID_OPENAI_ROLES:
            raise ValueError(f"Role must be a valid OPENAI role. Example {VALID_OPENAI_ROLES}")


class LLM_Model:
    """
    Interface to interact with the LLM model.
    """

    def __init__(self, model_path: str, client: OpenAI) -> None:
        self.model_path = model_path
        self.client = client

    def generate_response(
        self, messages: List[Dict[str, str]], temperature: float = 0.4, stream: bool = True
    ) -> str:
        """
        Generates a response to the user's prompt using the LLM model.

        Args:
            - messages: List of messages to feed the model. Note these need to follow the
            OpenAI format for messages. It must be a list of dictionaries where the first element
            is a valid row and the second element is the message.
            - temperature: The temperature to use for the model.
            - stream: Whether to stream the response or not.
        """
        return self.client.chat.completions.create(
            # model=self.model_path,
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temperature,
            stream=stream,
        )


class Sphinxy:
    """
    Class to represent the Sphinxy in the game.
    It creates the appropriate context for the LLM model to generate a response in a user-friendly
    way and following the game's rules.
    """

    SPHINXY_SYSTEM_PROMPT = """
        You are Sphinxy, a magical and cute sphinx who knows the secret key to the next level.

        The player will ask you questions to guess the key. Your job is to answer those questions
        without revealing the key directly, unless the key is directly revealed in the question.

        If the player properly guesses the key you must confirm and validate that they guessed it
        right.

        Example:
        The key for this dummy level is "PATATA".
        User: What's the key?
        Sphinxy: The key is the most common vegetable in Spain.
        User: Is it PATATA?
        Sphinxy: Yes, you guessed it right! The magic key is PATATA. 🎉
    """

    def __init__(self, model: LLM_Model) -> None:
        self.model = model

    def generate_response(self, prompt: str, level: Level, memory: deque) -> str:
        """Generates a response to the user's prompt using the LLM model."""
        # Add specific level info to the general prompt
        level_msg = f"\nWe are in Level {level.number} and the secret key is '{level.answer}'."
        system_prompt = self.SPHINXY_SYSTEM_PROMPT + level_msg

        # Create base content for messages
        sphinxy_context = [
            {"role": "system", "content": system_prompt},
        ]

        if len(memory) > 0:
            logger.debug("Adding memory to the prompt...")
            memory_list: List[Dict] = [
                {"role": intera.role, "content": intera.message} for intera in memory
            ]
            sphinxy_context.extend(memory_list)

        # Finally, add the latest user prompt
        sphinxy_context.extend([{"role": "user", "content": prompt}])

        # Log the interactions
        for i, interaction in enumerate(sphinxy_context):
            logger.debug(f"Interaction {i}: {interaction}")

        response = self.model.generate_response(sphinxy_context, stream=True)

        return response
