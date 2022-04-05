
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
    def __init__(self, socket: str):
        self.socket: socket.socket = socket

    def send_error(self, exception: HFTPException):
        print(type(exception))
        print(f"error_code: {exception.error_code}")  # FIXME

        # TODO Read send and recvfrom_into
        # El comando "get_file_listing" no retorna con \r\n
        # por lo que este comando genérico funciona para todos los casos
        self.send_response(
            exception.error_code,
            Command("dismiss", [])
        )

    def send_response(self, code: int, command: Command, lines: list = []):
        print("send_response()")  # FIXME

        name_command: Command = command.name

        self.send_line(f"{code} {constants.code_messages[code]}")

        for line in lines:
            self.send_line(line)

        if(name_command == "get_file_listing"):
            self.send_line("")

    def send_line(self, line: str):
        print(f"line: {line}")  # FIXME
        self.socket.send((line + "\r\n").encode("ascii"))
