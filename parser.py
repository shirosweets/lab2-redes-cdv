import socket

import constants
from command import Command
from HFTP_Exception import MalformedParserException, UnknownParserException


class Parser(object):
    """
    Parsea los mensajes obtenidos mediante la conexión por un socket.
    """

    def __init__(self, socket: socket.socket):
        print("__init__ PARSER")  # FIXME
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
            print(f"Current byte: {current_byte}")  # FIXME
            command_str = command_str + current_byte.decode("ascii")
            print(f"Current command: {command_str}")  # FIXME

        if (command_str[-2:-1] == "\r"):
            # Eliminamos '\r\n\'
            words = command_str.split(" ")
            print(f"words: {words}")  # FIXME
            words[-1] = words[-1].strip("\r\n")
            print(f"words: {words}")  # FIXME

        else:
            # Comando malformado, levantamos un error
            raise MalformedParserException(f"Parser Error: {constants.PARSER_STATUS_MALFORMED}")

        command = Command(words[0], words[1:])
        return command
