import sys

from InGaTools.handler_msg.constants import Color


class HandlerMsg:
    """Handler msg class."""

    @staticmethod
    def write_msg(color: str, msg: str) -> None:
        """Write msg to screen.

        Args:
            color (str)
            msg (str): message.
        """
        sys.stdout.write(f"{color}{msg}{Color.WHITE.value}\n")

    def white(self, msg, *args):
        self.write_msg(Color.WHITE.value, msg % args)

    def green(self, msg, *args):
        self.write_msg(Color.GREEN.value, msg % args)

    def red(self, msg, *args):
        self.write_msg(Color.RED.value, msg % args)

    def blue(self, msg, *args):
        self.write_msg(Color.BLUE.value, msg % args)

    def magenta(self, msg, *args):
        self.write_msg(Color.MAGENTA.value, msg % args)

    def yellow(self, msg, *args):
        self.write_msg(Color.YELLOW.value, msg % args)

    def cyan(self, msg, *args):
        self.write_msg(Color.CYAN.value, msg % args)

    def info(self, msg, *args):
        self.white(msg, *args)

    def debug(self, msg, *args):
        self.white(msg, *args)

    def warning(self, msg, *args):
        self.yellow(msg, *args)

    def error(self, msg, *args):
        self.red(msg, *args)


handler_msg = HandlerMsg()
