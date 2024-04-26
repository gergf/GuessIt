from pathlib import Path

import requests

from log_config import setup_logger

logger = setup_logger()

# Move to config
MODEL_URL: str = "https://huggingface.co/lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF/resolve/main/Meta-Llama-3-8B-Instruct-Q8_0.gguf"  # noqa


def download_file(url: str, save_path: Path):
    """
    Downloads the file in the given URL and saves it locally.
    """
    # Check dirs to local_filename exists, if not create it
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)

    with requests.get(url, stream=True) as r:
        # Raise an exception in case of an unsuccessful request
        r.raise_for_status()
        with open(save_path, "wb") as f:
            # Write the contents of the response to the file in chunks
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def ping_server(url: str) -> bool:
    """
    Pings the server at the given URL to check if it is running.
    """
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


# TODO: Move to utils
def check_requirements(model_path: Path, llm_server_url: str):
    """Checks if the required models are available."""
    logger.info("Checking LLM model is present in the local filesystem...")
    if not model_path.exists():
        logger.warning(f"Model not found: {model_path}. Downloading...")
        download_file(url=MODEL_URL, save_path=model_path)
        logger.info(f"Model saved into: {model_path}")
    else:
        logger.info(f"Model OK ✅ ({model_path})")

    logger.info("Checking local LLM server is running...")
    LLM_SERVER_UP = ping_server(llm_server_url + "health")
    if not LLM_SERVER_UP:
        logger.error("LLM server not running. Please start the server before running the game.")
        # raise Exception("LLM server not running.")
    else:
        logger.info("LLM server OK ✅")

    logger.info("All requirements are met.")
