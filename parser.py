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

    def __init__(self, socket: socket.socket):
        logger.log_debug("__init__ PARSER")
        self.socket = socket
        self.status = constants.PARSER_STATUS_OK

    def get_next_command(self):
        """
        Obtiene y devuelve el comando de un socket.

        Los comandos deben finalizar en `\\r\\n`
        """
        command_str = ""

        # Buscamos '\n'
        while not command_str.endswith("\n"):
            current_byte = self.socket.recv(1)
            command_str = command_str + current_byte.decode("ascii")

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
            # Comando malformado, levantamos un error
            raise MalformedParserException()

        command = Command(words[0], words[1:])
        return command
