# Command Handler
import constants

from command import Command


class Handler():
    """
    Manejador de comandos.
    """
    def __init__(self, command: Command):
        self.command = command
        self.status = constants.HANDLER_STATUS_OK

    def handle(self):
        """
        Ejecuta un comando.
        """
        print(f">> Executing command: {self.command.name} {' '.join(self.command.arguments)}")
