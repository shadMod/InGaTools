import logging
import sys
from http.client import HTTPResponse
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, build_opener

import requests

from InGaTools.core.constants import (
    KEYBORD_EXCEPT,
    LINK_REGEX,
    MOZILLA_USER_AGENT,
    MSG_INFO,
)
from InGaTools.handler_msg.handler_msg import handler_msg
from InGaTools.handler_msg.log_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)


class CrawlerTool:
    """Crawler tool class."""

    def __init__(self, url: str, limit: int = 0, crawl_depth: int = 50):
        """Init crawler tool class.

        Args:
            url (str): Target URL.
            limit (int): Maximum number of crawl requests to perform.
            crawl_depth (int): Depth of crawling process.
        """
        self.log = None
        self.output_name = None
        self._url: str = url

        self.__user: str = "admin"
        self.__password: str = "password"
        self.__crawl_limit: int = limit
        self.__crawl_limit_flag: bool = True if limit > 0 else False
        self.__crawl_depth: int = crawl_depth + 3 if crawl_depth > 0 else crawl_depth

        self.__directories = []
        self.__indexing = []
        self.__externals_url_vector = []
        self.__files_vector = []
        self.__extensions_found = []
        self.__output_name = ""
        self.__output_file = ""

    def crawl(self, url_to_crawl: str | list) -> tuple[list[str], list[str], list[tuple[str, str]]]:
        """Crawl target URL.

        Args:
            url_to_crawl (str | list): Target URL/s.

        Returns:
            tuple[list[str], list[str], list[tuple[str, str]]]: Add me.
        """
        crawled = []
        not_crawled = []
        files = []

        if isinstance(url_to_crawl, list):
            urls_to_crawl = url_to_crawl
        elif isinstance(url_to_crawl, str):
            urls_to_crawl = [url_to_crawl]
        else:
            raise Exception("url_to_crawl should be a string or a list")

        try:
            while urls_to_crawl:
                if self.__crawl_limit_flag:
                    if len(crawled) >= self.__crawl_limit:
                        break
                url = urls_to_crawl.pop(0)
                if self.__crawl_depth > 0:
                    if url.endswith("/"):
                        if url.rpartition("/")[0].count("/") >= self.__crawl_depth:
                            continue
                    elif url.count("/") >= self.__crawl_depth:
                        continue
                logger.debug("Add %s in crawled.", url)
                crawled.append(url)
                parsed_url = urlparse(url)
                host = parsed_url.scheme + "://" + parsed_url.netloc
                if parsed_url.path.endswith("/"):
                    link_path = host + parsed_url.path
                else:
                    link_path = host + parsed_url.path.rpartition("/")[0] + "/"
                response = self.getting_url(url)
                if response:
                    content = response.read()
                    url_content_type = response.headers.get("content-type")
                    if url_content_type:
                        if "text/html" not in url_content_type and url not in files:
                            url_type = url_content_type.split(";")[0].split("/")[1]
                            files.append((url, url_type))
                        else:
                            links_extracted = self.clean_and_strip_links(host, link_path, content)
                            if links_extracted is None:
                                raise Exception("Error while clean and strip links extracted.")
                            links_extracted.sort()
                            for link in links_extracted:
                                parsed_link = urlparse(link)
                                link_host = parsed_link.scheme + "://" + parsed_link.netloc
                                if link_host == host:
                                    if link not in crawled and link not in urls_to_crawl:
                                        urls_to_crawl.append(link)
                                elif link not in not_crawled:
                                    not_crawled.append(link)
        except KeyboardInterrupt:
            raise KeyboardInterrupt(KEYBORD_EXCEPT)
        except Exception as error:
            raise Exception(error)
        else:
            return crawled, not_crawled, files

    @staticmethod
    def getting_url(url: str) -> HTTPResponse | None:
        """Open and get response from url.

        Args:
            url (str): Target URL.

        Returns:
            HTTPResponse | None: If there are no errors: return the response, otherwise None.
        """
        try:
            request = Request(url)
            request.add_header("User-Agent", MOZILLA_USER_AGENT)
            request.get_method = lambda: "GET"
            opener_web = build_opener()
            response = opener_web.open(request)
            opener_web.close()
        except HTTPError as error_code:
            logger.error(error_code.getcode())
            return None
        except URLError as error_code:
            logger.error(error_code.args[0][0])
            return None
        except Exception as error:
            logger.error("Error while getting url, reason: %s\n", error)
            return None
        else:
            return response

    @staticmethod
    def clean_and_strip_links(host: str, path: str, content: str) -> list | None:
        """Clean and strip the links contained in the content.

        Args:
            host (str): Target host URL.
            path (str): Target path URL.
            content (str): Content of the URL.

        Returns:
            list | None: If there are no errors: return clean links, otherwise None.
        """
        try:
            links = LINK_REGEX.findall(content)
            for link in links:
                link_strip = link.strip(" ")
                parsed_link = urlparse(link_strip)
                if not parsed_link.scheme and not parsed_link.netloc:
                    if link_strip.startswith("/"):
                        if host.endswith("/"):
                            links[links.index(link)] = host.rstrip("/") + link_strip
                        else:
                            links[links.index(link)] = host + link_strip
                    elif link_strip.startswith("./"):
                        links[links.index(link)] = host + link_strip
                    else:
                        links[links.index(link)] = path + link_strip
                else:
                    links[links.index(link)] = link_strip
            for link in links:
                links[links.index(link)] = link.split("#")[0]
        except Exception as error:
            handler_msg.error(f"Error while getting links, reason: {error}")
            return None
        else:
            return links

    def search_indexing_pages(self, links_vector: list[str]) -> tuple[list, list]:
        """Search indexing pages.

        Args:
            links_vector (list[str]): List of links.

        Returns:
            tuple[list, list]: Add me.
        """
        directories = []
        indexing_pages = []
        title_position_end = -1
        title = ""
        try:
            for link in links_vector:
                while len(link.split("/")) > 4:
                    link = link.rpartition("/")[0]
                    if (link + "/") not in directories:
                        directories.append(link + "/")
            directories.sort()
            handler_msg.green(f"{len(directories)} directories found: {", ".join(directories)}")
            dots = "."
            for directory in directories:
                sys.stdout.flush()
                sys.stdout.write("\r\x1b" + dots)
                if len(dots) > 30:
                    dots = "."
                dots = dots + "."
                response = self.getting_url(directory)
                if response:
                    content = response.read()
                    title_position_start = content.find("<title>")
                    title_position_start_more = title_position_start + 7
                    if title_position_start != -1:
                        title_position_end = content.find("</title>", title_position_start_more)
                    if title_position_end != -1:
                        title = content[title_position_start_more:title_position_end]
                    if title:
                        if title.find("Index of") != -1:
                            indexing_pages.append(directory)
        except Exception as error:
            error_msg = f"Error while run search_indexing_pages, reason: {error}."
            logger.error("%s", error_msg)
            raise Exception(error_msg)
        else:
            if indexing_pages:
                handler_msg.green(f"{len(indexing_pages)} directories with indexing: {", ".join(indexing_pages)}")
            else:
                handler_msg.yellow("No directory with indexing")
            return directories, indexing_pages

    @staticmethod
    def external_links(root_url: str, external_vector: list[str]) -> list[str]:
        """Get all external links.

        Args:
            root_url (str): Root URL.
            external_vector (list[str]): List of external vectors.

        Returns:
            list[str]: All external links.
        """
        external_websites = []
        try:
            parsed_url = urlparse(root_url)
            domain = parsed_url.netloc.split("www.")[-1]
            # get all subdomain
            subdomain_list = []
            for link in external_vector:
                parsed = urlparse(link)
                if domain in parsed.netloc:
                    subdomain = parsed.scheme + "://" + parsed.netloc
                    if subdomain not in subdomain_list:
                        subdomain_list.append(subdomain)
            handler_msg.green(f"{len(subdomain_list)} subdomains found: {", ".join(subdomain_list)}.")
            # get all email
            email_list = []
            for link in external_vector:
                if "mailto" in urlparse(link).scheme:
                    email_list.append(link.split(":")[1].split("?")[0])
            handler_msg.green(f"{len(email_list)}  emails found: {", ".join(email_list)}.")
            # get all external vector
            for link in external_vector:
                parsed = urlparse(link)
                if parsed.netloc:
                    if domain not in parsed.netloc:
                        external_domain = parsed.scheme + "://" + parsed.netloc
                        if external_domain not in external_websites:
                            external_websites.append(external_domain)
            external_websites.sort()
            handler_msg.green(f"{MSG_INFO} {", ".join(external_websites)}")
        except Exception as error:
            error_msg = f"Error while run external_links, reason: {error}."
            logger.error("%s", error_msg)
            raise Exception(error_msg)
        return external_websites

    @staticmethod
    def statistics(links_crawled: list[str], files):
        amt_files_per_extension = {}
        try:
            if len(links_crawled) > 1:
                for _, extension in files:
                    if extension not in amt_files_per_extension:
                        amt_files_per_extension[extension] = 0
                    else:
                        amt_files_per_extension[extension] += 1
                handler_msg.green(f"{len(files)} files found.")
                for extension in amt_files_per_extension.keys():
                    handler_msg.green(f"\t{extension} ~ {amt_files_per_extension[extension]};")
        except Exception as error:
            logger.error("Error while run external_links, reason: %s.", error)

    def run_crawler_tool(self):
        try:
            response = requests.get(self._url)
            url_to_crawl = response.url
            logger.info(url_to_crawl)
        except Exception as error:
            error_msg = f"Error on getting response, reason: {error}."
            logger.error(error_msg)
            raise Exception(error_msg)
        try:
            links_crawled, links_not_crawled, files = self.crawl(url_to_crawl)
            self.search_indexing_pages(links_crawled)
            self.external_links(url_to_crawl, links_not_crawled)
            self.statistics(links_crawled, files)
        except KeyboardInterrupt:
            logger.error(KEYBORD_EXCEPT)
            raise Exception(KEYBORD_EXCEPT)
        except Exception as error:
            error_msg = f"Error while run crawler tool, reason: {error}."
            logger.error(error_msg)
            raise Exception(error_msg)
