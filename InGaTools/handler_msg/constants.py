from enum import Enum


class Color(Enum):
    WHITE = "\033[1;37m"
    GREEN = "\033[1;32m"
    RED = "\033[1;31m"
    BLUE = "\033[1;34m"
    MAGENTA = "\033[1;35m"
    YELLOW = "\033[1;33m"
    CYAN = "\033[1;36m"
    NORMAL = "\033[0m"
    UNDERLINE = "\033[4m"
