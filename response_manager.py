
import socket
import constants

from click import command
from command import Command
from HFTP_Exception import HFTPException

class ResponseManager():
    """
    Manejador de respuestas, se encarga de enviar
    por socket las respuestas correspondientes a cada comando
    y código de mensaje.
    """
    def __init__(self, socket: str, command: Command):
        self.socket: socket.socket = socket
        self.name_command: Command = command.name

    def send_error(self, exception: HFTPException):
        print(f"error_code: {error_code}")  # FIXME

        constants.error_messages[exception.error_code]
        # TODO Read send and recvfrom_into

    def send_response(self, code: int, lines: list = []):
        print("send_response()")  # FIXME

        self.socket.send(f"{code} {constants.error_messages[code]}\r\n")

        for line in lines:
            self.socket.send(line + "\r\n")

        if(self.name_command == "get_file_listing"):
            self.socket.send("\r\n")
