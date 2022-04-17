
import errno
import socket
import constants

from logger import Logger
from command import Command
from hftp_exception import HFTPException

logger = Logger()


class ResponseManager():
    """
    Manejador de respuestas, se encarga de enviar
    por socket las respuestas correspondientes a cada comando
    y código de mensaje.
    """
    def __init__(self, socket: str):
        self.socket: socket.socket = socket

    def send_error(self, exception: HFTPException):
        logger.log_debug(f"Exception type: {type(exception)}")
        logger.log_error(f"error_code: {exception.error_code}")

        # TODO Read send and recvfrom_into
        # El comando "get_file_listing" no retorna con \r\n
        # por lo que este comando genérico funciona para todos los casos
        self.send_response(
            exception.error_code,
            Command("dismiss", []),
            []
        )

    def send_response(self, code: int, command: Command, lines: list = []):
        logger.log_debug("send_response()")

        name_command: Command = command.name

        self.send_line(f"{code} {constants.code_messages[code]}")

        for line in lines:
            self.send_line(line)

        if(name_command == "get_file_listing"):
            self.send_line("")

    def send_line(self, line: str):
        logger.log_info(f"line: {line}")

        try:
            self.socket.send((line + "\r\n").encode("ascii"))
        except IOError as error:
            if error.errno == errno.EPIPE:
                # Handle the error
                logger.log_error("send_line() - PIPE ERROR")
                raise error
