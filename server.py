#!/usr/bin/env python
# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Revisión 2014 Carlos Bederián
# Revisión 2011 Nicolás Wolovick
# Copyright 2008-2010 Natalia Bidart y Daniel Moisset
# $Id: server.py 656 2013-03-18 23:49:11Z bc $

import sys
import logging
import socket
import optparse
import constants

from logger import Logger
from connection import Connection


class Server(object):
    """
    El servidor, que crea y atiende el socket en la dirección y puerto
    especificados donde se reciben nuevas conexiones de clientes.
    """

    def __init__(
        self,
        addr=constants.DEFAULT_ADDR,
        port=constants.DEFAULT_PORT,
        directory=constants.DEFAULT_DIR
    ):
        print("Serving %s on %s:%s." % (directory, addr, port))

        self.directory = directory

        # Creación del socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Configuración
        self.socket.bind((addr, port))

        # Listening
        self.socket.listen(1)

    def serve(self):
        """
        Loop principal del servidor. Se acepta una conexión a la vez
        y se espera a que concluya antes de seguir.
        """
        while True:
            # Aceptar una conexión al server, crear una
            # connection para la conexión y atenderla hasta que termine.
            connection = Connection(self.socket.accept()[0], self.directory)
            connection.handle()


def main():
    """Parsea los argumentos y lanza el server"""

    parser = optparse.OptionParser()
    parser.add_option(
        "-p", "--port",
        help="Número de puerto TCP donde escuchar",
        default=constants.DEFAULT_PORT
    )

    parser.add_option(
        "-a", "--address",
        help="Dirección donde escuchar",
        default=constants.DEFAULT_ADDR
    )

    parser.add_option(
        "-d", "--datadir",
        help="Directorio compartido",
        default=constants.DEFAULT_DIR
    )

    parser.add_option(
        "-v", "--verbose",
        dest="level",
        action="store",
        help="Determina cuanta información de depuración mostrar"
        "(valores posibles son: ERROR, WARN, INFO, DEBUG)",
        default="ERROR"
    )

    options, args = parser.parse_args()
    setup_logger(options.level)

    if len(args) > 0:
        parser.print_help()
        sys.exit(1)
    try:
        port = int(options.port)
    except ValueError:
        sys.stderr.write(
            "Numero de puerto invalido: %s\n" % repr(options.port))
        parser.print_help()
        sys.exit(1)

    server = Server(options.address, port, options.datadir)
    server.serve()


def setup_logger(level):
    DEBUG_LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARN': logging.WARNING,
        'ERROR': logging.ERROR,
    }

    # Setar verbosidad
    code_level = DEBUG_LEVELS.get(level)  # convertir el str en codigo
    logging.basicConfig(format='[%(levelname)s] - %(message)s')
    logger = Logger()
    logger._logger.setLevel(code_level)


if __name__ == '__main__':
    main()
