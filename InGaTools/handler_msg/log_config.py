import logging

from InGaTools.core.settings import LOG_LEVEL


def setup_logging():
    """Sets up the logging module."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        # format="%(asctime)s [%(levelname)s]: %(name)s - %(message)s",
        format="%(message)s",
        handlers=[logging.StreamHandler()],
    )
    # logger = logging.getLogger("log-tools")
    # logging.basicConfig(filename='logs/tools.log', encoding='utf-8', level=logging.DEBUG, format=format_)
    # logger.setLevel(logging.DEBUG)
