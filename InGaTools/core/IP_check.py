import logging
import socket
import sys

from InGaTools.core.constants import INFO_HELP, INVALID_URL_IP, RETRY_PLS
from InGaTools.core.utils import quick_clear_console
from InGaTools.handler_msg.handler_msg import handler_msg
from InGaTools.reco_menu.reco_menu import RecoMenu

logger = logging.getLogger(__name__)


class IPCheck:
    """IP check class."""

    def __init__(self, target: str):
        """Init the IPCheck class.

        Args:
            target (str): Target IP address.
        """
        self._domain, self._url = self.clean_target(target)
        quick_clear_console()
        handler_msg.blue(INFO_HELP)

    @staticmethod
    def clean_target(target: str) -> tuple[str, str]:
        """Clean the target IP address.

        Args:
            target (str): Target IP address.

        Returns:
            tuple[str, str]: Domain address and target address.
        """
        if "http" in target:
            domain = target.split("//")[1]
        elif "http" not in target:
            domain = target
            target = f"https://{target}"
        else:
            handler_msg.red(INVALID_URL_IP)
            sys.exit(1)
        return domain, target

    def run_ip_check(self) -> None:
        """Run IP check."""
        try:
            ip = socket.gethostbyname(self._domain)
            RecoMenu(self._domain, self._url, ip).run()
        except Exception as error:
            logger.error("%s\n\nReason: %s", RETRY_PLS, error)
            sys.exit(1)
