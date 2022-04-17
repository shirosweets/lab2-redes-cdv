import socket
import constants

from logger import Logger
from command import Command
from hftp_exception import MalformedParserException, UnknownParserException

logger = Logger()


class Parser(object):
    """
    Parsea los mensajes obtenidos mediante la conexión por un socket.
    """
    PARSER_BUFFER_SIZE = 2 ** 12  # in bytes

    def __init__(self, socket: socket.socket):
        logger.log_debug("__init__ PARSER")

        self.buffer = list()
        self.socket = socket
        self.status = constants.PARSER_STATUS_OK

    def read_byte(self) -> chr:
        try:
            logger.log_debug(f"read_byte() buffer: {self.buffer}")

            # if(self.buffer.pop(0) == '\\x00')

            return chr(self.buffer.pop(0))
        except IndexError:
            self.buffer.extend(self.socket.recv(self.PARSER_BUFFER_SIZE))
            logger.log_debug(
                f"{len(self.buffer)} bytes fetched from socket."
                f" Current buffer: {self.buffer}"
            )
            return chr(self.buffer.pop(0))

    def get_next_command(self):
        """
        Obtiene y devuelve el comando de un socket.

        Los comandos deben finalizar en `\\r\\n`
        """
        logger.log_debug("Executing get_next_command()")

        command_str = ""

        # Buscamos '\n'
        while not command_str.endswith("\n"):
            current_byte = self.read_byte()
            command_str = command_str + current_byte

            logger.log_debug(
                f"Current byte: {current_byte} - "
                f"current command: {command_str}")

        if (command_str[-2:-1] == "\r"):
            # Eliminamos '\r\n\'
            words = command_str.split(" ")
            logger.log_debug(f"command_str.split: {words}")

            words[-1] = words[-1].strip("\r\n")
            logger.log_info(f"words: {words}")
        else:
            logger.log_warning("Malformed command. Raising exception")
            raise MalformedParserException()

        command = Command(words[0], words[1:])
        return command
