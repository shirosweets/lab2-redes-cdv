from http import client
from logging import exception
import sys
import os
import base64
import constants

from client import Client
from asyncore import read
from command import Command
from HFTP_Exception import HFTPException


class Handler():
    """
    Manejador de comandos.
    """
    def __init__(self, command: Command):
        self.command: Command = command
        self.status = constants.HANDLER_STATUS_OK

    def handle(self):
        """
        Ejecuta un comando válido.

        Si recibe un comando inválido levanta una excepción y finaliza.
        """
        print(f">> Executing command: {self.command.name} {' '.join(self.command.arguments)}")

        # Corroboramos si el comando es válido
        if (self.command.name == self.command.COMMAND_GET_FILE_LISTING):
            return self.handle_get_file_listing()
        elif (self.command.name == self.command.COMMAND_GET_METADATA):
            return self.handle_get_metadata()
        elif (self.command.name == self.command.COMMAND_GET_SLICE):
            return self.handle_get_slice()
        elif (self.command.name == self.command.COMMAND_QUIT):
            return self.handle_quit()
        else:
            # No encontró ningún comando válido...
            exception = HFTPException(
                constants.INVALID_COMMAND,
                "Invalid Command",
                constants.HANDLER_INVALID_COMMAND
            )
            raise exception

    def handle_get_file_listing(self):
        """
        Ejecuta el comando `get_file_listing`
        """
        if(len(self.command.arguments) == 0):
            directory = os.listdir()
        else:
            exception = HFTPException(constants.INVALID_ARGUMENTS,
                    "Invalid amount of arguments")
            self.status = constants.HANDLER_INVALID_COMMAND
            raise exception
        return directory

    def handle_get_metadata(self):
        """
        Ejecuta el comando `get_metadata`
        """
        if (len(self.command.arguments) == 1):
            size = os.path.getsize(self.command.arguments[0])
        else:
            exception = HFTPException(constants.INVALID_ARGUMENTS,
                    "Invalid amount of arguments")
            self.status = constants.HANDLER_INVALID_COMMAND
            raise exception
        return size

    def handle_get_slice(self):
        """
        Ejecuta el comando `get_slice`
        """
        if (len(self.command.arguments) == 3 ):
            file_size = os.path.getsize(self.command.arguments[0])
            request_size = self.command.arguments[1]+self.command.arguments[2]
            if (file_size >= request_size):
                file = open(self.command.arguments[0],"r")
                data = base64.b64encode(read(file, request_size))
            else:
                exception = HFTPException(constants.BAD_OFFSET,
                        "Amount of bytes out of bounds")
                self.status = constants.HANDLER_INVALID_COMMAND
                raise exception
        else:
            exception = HFTPException(constants.INVALID_ARGUMENTS,
                    "Amount of arguments must be 3")
            self.status = constants.HANDLER_INVALID_COMMAND
            raise exception
        return data
        # TODO @Ernesto

    def handle_quit(self):
        """
        Ejecuta el comando `quit`
        """
        self.status = constants.HANDLER_STATUS_EXIT
