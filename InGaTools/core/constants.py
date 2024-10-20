# flake8: noqa
import re

INFO_HELP = """
    --------------------------------------------------
                #    #   ####    #####      
                #    #  #    #  #
                ######  #    #  #
                #    #  #    #  #
                #    #  #    #  #
                #    #   ####    #####

        Version: 2.0
        By Shadmod - info@shadmod.it
        Thanks Team Hackersonlineclub
        Website : https://hackersonlineclub.com
    --------------------------------------------------
"""

# ----------------------------------- ERROR LIST ------------------------------------------
KEYBORD_EXCEPT = "Keyboard Interruption! Exiting..."
RETRY_PLS = "Wrong target not able to get IP address. Please retry."
MSG_INFO = "This website have references to the following websites:"
INVALID_URL_IP = "Error: Invalid URL / IP Entered."
MOZILLA_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
LINK_REGEX = re.compile(
    '[^>](?:href\=|src\=|content\="http)[\'*|"*](.*?)[\'|"].*?>',
    re.IGNORECASE,
)
