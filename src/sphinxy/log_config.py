import logging

logger = None


def setup_logger():
    global logger
    if logger is not None:
        return logger
    logging.basicConfig(
        filename="game.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)
    return logger
