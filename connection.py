# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Copyright 2014 Carlos Bederián
# $Id: connection.py 455 2011-05-01 00:32:09Z carlos $

# Imports de librerías
import socket
from base64 import b64encode
from HFTP_Exception import InternalErrorException


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

                # Instancia de Handler
                handler = Handler(command)

                # Procedimiento para atender el comando
                handler.handle()

                if handler.status == constants.HANDLER_STATUS_EXIT:
                    break
        except Exception as exception:
            print(
                f"CODE ERROR: {constants.INTERNAL_ERROR} - "
                f"Internal Error. Exception: {exception}"
            )
            response_manager.send_error(InternalErrorException(exception))

        # Cierra la conexión
        self.socket.close()

        print(f"END handle")  # FIXME
