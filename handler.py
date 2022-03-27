import sys
import constants
from HFTP_Exception import HFTPException

from command import Command


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
            self.handle_get_file_listing()
        elif (self.command.name == self.command.COMMAND_GET_METADATA):
            self.handle_get_metadata()
        elif (self.command.name == self.command.COMMAND_GET_SLICE):
            self.handle_get_slice()
        elif (self.command.name == self.command.COMMAND_QUIT):
            self.handle_quit()
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
        pass

    def handle_get_metadata(self):
        """
        Ejecuta el comando `get_metadata`
        """
        pass

    def handle_get_slice(self):
        """
        Ejecuta el comando `get_slice`
        """
        # TODO @Ernesto
        pass

    def handle_quit(self):
        """
        Ejecuta el comando `quit`
        """
        self.status = constants.HANDLER_STATUS_EXIT
