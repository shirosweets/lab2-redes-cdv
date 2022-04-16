# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Copyright 2014 Carlos Bederián
# $Id: connection.py 455 2011-05-01 00:32:09Z carlos $

# Imports de librerías
import socket
import traceback
from base64 import b64encode
from hftp_exception import HFTPException, InternalErrorException

# Imports locales
import constants
from logger import Logger
from handler import Handler
from response_manager import ResponseManager
from parser import Parser, MalformedParserException, UnknownParserException

logger = Logger()


class Connection(object):
    """
    Conexión punto a punto entre el servidor y un cliente.
    Se encarga de satisfacer los pedidos del cliente hasta
    que termina la conexión.
    """

    def __init__(self, socket, directory):
        self.socket = socket
        self.current_directory = directory

    def handle(self):
        """
        Atiende eventos de la conexión hasta que termina.
        """
        logger.log_info(f"START handle")

        # Instanciamos Parser
        parser = Parser(self.socket)

        # Instanciamos ResponseManager
        response_manager = ResponseManager(self.socket)

        # Atiende todos los comandos hasta que encuentra un fin de línea
        try:
            response = []
            while True:
                try:
                    # Obtenemos el comando parseado
                    command = parser.get_next_command()
                except MalformedParserException as malformedException:
                    logger.log_info(f"{malformedException}")
                    response_manager.send_error(malformedException)
                    break

                except UnknownParserException as UnknownException:
                    logger.log_info(f"{UnknownException}")
                    response_manager.send_error(UnknownException)
                    break

                try:
                    # Instancia de Handler
                    handler = Handler(command, self.current_directory)
                    logger.log_info(f"handler.status = {handler.status}")

                    # Procedimiento para atender el comando
                    response = handler.handle()
                    logger.log_info(
                        f"response in connection.py = {response} "
                        f"of type: {type(response)}")
                except HFTPException as hftpException:
                    response_manager.send_error(hftpException)

                logger.log_info(f"response_manager.send_response()")

                response_manager.send_response(
                    constants.CODE_OK,
                    command,
                    response
                )

                logger.log_info(f"handler.status = {handler.status}")

                if handler.status == constants.HANDLER_STATUS_EXIT:
                    logger.log_error(
                        f"handler status is '{constants.HANDLER_STATUS_EXIT}'."
                        " Closing socket")
                    break

        except Exception as exception:
            logger.log_error(
                f"CODE ERROR: {constants.INTERNAL_ERROR} - "
                f"Internal Error. Exception: {exception}"
            )
            traceback.print_exc()
            try:
                response_manager.send_error(InternalErrorException(exception))
            except BrokenPipeError:
                logger.log_error(
                    "Could not send error message because "
                    "Socket connection was lost")

        # Cierra la conexión
        self.socket.close()

        logger.log_info(f"END handle")  # FIXME
