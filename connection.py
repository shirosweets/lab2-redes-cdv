# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Copyright 2014 Carlos Bederián
# $Id: connection.py 455 2011-05-01 00:32:09Z carlos $

# Imports de librerías
import socket
import traceback
from base64 import b64encode
from HFTP_Exception import HFTPException, InternalErrorException


# Imports locales
import constants
from parser import Parser, MalformedParserException, UnknownParserException
from handler import Handler
from response_manager import ResponseManager


class Connection(object):
    """
    Conexión punto a punto entre el servidor y un cliente.
    Se encarga de satisfacer los pedidos del cliente hasta
    que termina la conexión.
    """

    def __init__(self, socket, directory):
        # NOTE FALTA Inicializar atributos de Connection
        self.socket = socket
        self.current_directory = directory

    def handle(self):
        """
        Atiende eventos de la conexión hasta que termina.
        """
        print(f"START handle")  # FIXME
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
                    print(f"{malformedException}")  # FIXME
                    response_manager.send_error(malformedException)
                    break

                except UnknownParserException as UnknownException:
                    print(f"{UnknownException}")  # FIXME
                    response_manager.send_error(UnknownException)
                    break

                try:
                    # Instancia de Handler
                    handler = Handler(command, self.current_directory)
                    print(f"handler.status = {handler.status}")  # FIXME
                    # Procedimiento para atender el comando
                    response = handler.handle()  # FIXME: Arreglar los multiples tipos
                    print(f"response in connection.py = {response} of type: {type(response)}")  # FIXME
                except HFTPException as hftpException:
                    response_manager.send_error(hftpException)

                print(f"response_manager.send_response()")  # FIXME

                response_manager.send_response(
                    constants.CODE_OK,
                    command,
                    response
                )

                print(f"handler.status = {handler.status}")  # FIXME

                if handler.status == constants.HANDLER_STATUS_EXIT:
                    print(f"handler status is '{constants.HANDLER_STATUS_EXIT}'. Closing socket")
                    break

        except Exception as exception:
            print(
                f"CODE ERROR: {constants.INTERNAL_ERROR} - "
                f"Internal Error. Exception: {exception}"
            )
            traceback.print_exc()
            try:
                response_manager.send_error(InternalErrorException(exception))
            except BrokenPipeError:
                print("Could not send error message because Socket connection was lost")

        # Cierra la conexión
        self.socket.close()

        print(f"END handle")  # FIXME
