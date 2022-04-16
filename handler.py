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
    def __init__(self, command: Command, base_dir: str):
        self.command: Command = command
        self.status = constants.HANDLER_STATUS_OK
        self.base_dir = base_dir

    def handle(self):
        """
        Ejecuta un comando válido.

        Si recibe un comando inválido levanta una excepción y finaliza.
        """
        self.status = constants.HANDLER_STATUS_OK
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
            directory = os.listdir(self.base_dir)
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
            path = self.base_dir + "/" + self.command.arguments[0]
            print(f"metadata path: {path}") # FIXME
            size = os.path.getsize(path)
        else:
            exception = HFTPException(constants.INVALID_ARGUMENTS,
                    "Invalid amount of arguments")
            self.status = constants.HANDLER_INVALID_COMMAND
            raise exception
        return_list = list()
        return_list.append(str(size))
        return return_list

    def handle_get_slice(self):
        """
        Ejecuta el comando `get_slice`
        """
        if (len(self.command.arguments) == 3 ):
            path = self.base_dir + "/" + self.command.arguments[0]
            file_size = os.path.getsize(path)
            request_size = int(
                self.command.arguments[1]) + int(self.command.arguments[2]
            )

            # print(f"request_size: {request_size}")  # FIXME
            if (file_size >= request_size):
                try:
                    with open(path, "r") as file:
                        # Bytes
                        encoded_read = file.read(request_size).encode('ascii')

                        # Se encodea en base64 para que entre en tipo ASCII
                        data = base64.b64encode(encoded_read).decode('ascii')

                        return_list = list()
                        return_list.append(data)
                        print(f"list(data) = {return_list}")
                except IOError as error:
                    print(f"error: {error}")
                    raise error
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
        return return_list

    def handle_quit(self):
        """
        Ejecuta el comando `quit`
        """
        print("handle_quit()")  # FIXME
        self.status = constants.HANDLER_STATUS_EXIT
        return list()
