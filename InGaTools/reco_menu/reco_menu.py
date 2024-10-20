import logging
import os
import socket
import ssl
from typing import Any

import ipwhois
import requests

from InGaTools.core.constants import KEYBORD_EXCEPT
from InGaTools.core.settings import VIRUS_TOTAL_API_KEY
from InGaTools.crawl_target.crawl_target import CrawlerTool
from InGaTools.handler_msg.handler_msg import handler_msg
from InGaTools.handler_msg.log_config import setup_logging
from InGaTools.reco_menu.constants import (
    CHOICE_NOT_ALLOWED,
    FINDER_URL,
    RECO_MENU,
    SSL_INFO_FIELD_LIST,
    SSL_KEY_ERROR,
    SSL_NOT_FOUND,
    WHOIS_LOOKUP_FIELD_LIST,
)

setup_logging()

logger = logging.getLogger(__name__)


class RecoMenu:
    """RecoMenu class."""

    def __init__(self, domain: str, url: str, ip_address: str) -> None:
        """Init RecoMenu class.

        Args:
            domain (str): Add me.
            url (str): Add me.
            ip_address (str): Add me.
        """
        self._domain: str = domain
        self._url: str = url
        self._ip_address: str = ip_address
        self._reco_choice: int = None

    @staticmethod
    def print_menu() -> None:
        """Print RecoMenu menu."""
        handler_msg.green(RECO_MENU)

    def get_header_information(self, verify: bool = True) -> None:
        """Get header information."""
        handler_msg.info("Headers:")
        response = requests.get(self._url, verify=verify, timeout=10)
        for headers_key, headers_value in response.headers.items():
            handler_msg.info(f"{headers_key}: {headers_value}")

    def _get_cert_informations(
        self,
    ) -> tuple[dict[str, tuple], dict[str, Any], dict[str, Any]]:
        """Get all information of certificate.

        Returns:
            tuple[dict[str, tuple], dict[str, Any], dict[str, Any]]: Return a tuple with all information,
                subject and issuer.
        """
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=self._domain) as ssl_socket:
            try:
                ssl_socket.connect((self._domain, 443))
                info = ssl_socket.getpeercert()
                subject = dict(subject[0] for subject in info["subject"])
                issuer = dict(issuer[0] for issuer in info["issuer"])
            except Exception as error:
                logger.debug("Try without an SSL certificate, reason: %s.", error)
                ctx = ssl._create_unverified_context()
                with ctx.wrap_socket(socket.socket(), server_hostname=self._domain) as new_ssl_socket:
                    new_ssl_socket.connect((self._domain, 443))
                info = ssl.get_server_certificate((self._domain, 443))
                tmp_cert_file = f"{self._domain}.pem"
                with open(tmp_cert_file, "w") as fn:
                    fn.write(info)
                cert_dict = ssl._ssl._test_decode_cert(tmp_cert_file)
                subject = dict(subject[0] for subject in cert_dict["subject"])
                issuer = dict(issuer[0] for issuer in cert_dict["issuer"])
                info = cert_dict
                os.remove(tmp_cert_file)
        return info, subject, issuer

    def get_ssl_certificate_information(self) -> None:
        """Get SSL Certificate information."""
        handler_msg.info("SSL certificate information:")
        try:
            info, subject, issuer = self._get_cert_informations()
            for subject_name, subject_value in subject.items():
                handler_msg.info("%s: %s.", subject_name, subject_value)
            for issuer_key, issuer_value in issuer.items():
                handler_msg.info("%s: %s.", issuer_key, issuer_value)
            for label, field in SSL_INFO_FIELD_LIST:
                handler_msg.info("%s: %s.", label, info[field])
        except KeyError as error:
            handler_msg.error("%s Reason: %s.", SSL_KEY_ERROR, error)
        except Exception as error:
            handler_msg.error("%s Reason: %s.", SSL_NOT_FOUND, error)

    def whois_lookup(self) -> None:
        """Whois Lookup."""
        handler_msg.info("Whois lookup:")
        try:
            Lookup = ipwhois.IPWhois(self._ip_address)
            results = Lookup.lookup_whois()
            for label, field in WHOIS_LOOKUP_FIELD_LIST:
                handler_msg.info("%s: %s.", label, results[field])
            for nets_key, nets_value in results["nets"][0].items():
                handler_msg.info("%s: %s.", nets_key, nets_value)
        except KeyboardInterrupt:
            handler_msg.error(KEYBORD_EXCEPT)
        except Exception as error:
            logger.error(error)

    def get_subdomains_website(self) -> None:
        """Get Sub-domain Website."""
        handler_msg.info("Sub-domain website:")
        if not VIRUS_TOTAL_API_KEY:
            handler_msg.info("API key not found.")
        params = {"apikey": VIRUS_TOTAL_API_KEY, "domain": self._domain}
        response = requests.get(FINDER_URL, params=params)
        data = response.json()
        if "subdomains" in data:
            subdomains = data["subdomains"]
            handler_msg.info(f"subdomains found: {subdomains}")
        else:
            handler_msg.info("No subdomains found for this: %s.", self._domain)

    def crawl_target_website(self) -> None:
        """Crawl Target Website."""
        handler_msg.info("Web crawler target:")
        CrawlerTool(self._url).run_crawler_tool()

    def get_all_available_options(self) -> None:
        """Get header and SSL certificate information with the list of all subdomains,
        get whois and crawl the target.
        """

    def run(self) -> None:
        """Run RecoMenu."""

        while True:
            self.print_menu()
            reco_choice: int = int(input("Enter your choice: >"))
            if not reco_choice or not isinstance(reco_choice, int) or reco_choice not in list(range(7)):
                handler_msg.error(CHOICE_NOT_ALLOWED)
            match reco_choice:
                case 0:
                    break
                case 1:
                    self.get_header_information()
                case 2:
                    self.get_ssl_certificate_information()
                case 3:
                    self.whois_lookup()
                case 4:
                    self.get_subdomains_website()
                case 5:
                    self.crawl_target_website()
                case 6:
                    self.get_all_available_options()
