import os
import client
import socket
import os.path
import logging
import unittest

DATADIR = 'testGlobal'
TIMEOUT = 3  # Una cantidad razonable de segundos para esperar respuestas


class TestBase(unittest.TestCase):

    # Entorno de testing ...
    def setUp(self):
        print("\nIn method %s:" % self._testMethodName)
        os.system('rm -rf %s' % DATADIR)
        os.mkdir(DATADIR)

    def tearDown(self):
        os.system('rm -rf %s' % DATADIR)
        if hasattr(self, 'client'):
            if self.client.connected:
                # Deshabilitar el logging al desconectar
                # Dado que en algunos casos de prueba forzamos a que
                # nos desconecten de mala manera
                logging.getLogger().setLevel('CRITICAL')
                try:
                    self.client.close()
                except socket.error:
                    pass  # Seguramente ya se desconecto del otro lado
                logging.getLogger().setLevel('WARNING')
            del self.client
        if hasattr(self, 'output_file'):
            if os.path.exists(self.output_file):
                os.remove(self.output_file)
            del self.output_file

    # Funciones auxiliares:
    def new_client(self):
        assert not hasattr(self, 'client')
        try:
            self.client = client.Client()
        except socket.error:
            self.fail("No se pudo establecer conexión al server")
        return self.client
