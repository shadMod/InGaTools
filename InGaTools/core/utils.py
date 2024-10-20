import logging
import os

logger = logging.getLogger(__name__)


def quick_clear_console() -> None:
    """Quick clear console before starting the program."""
    try:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
    except Exception as error:
        logger.error(error)
