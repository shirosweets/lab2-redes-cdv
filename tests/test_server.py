import os
import time
import os.path
import select
import socket
import constants

from tests.test_base import TIMEOUT
from tests.test_base import DATADIR
from tests.test_base import TestBase


class TestHFTPServer(TestBase):

    # Tests
    def test_connect_and_quit(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((constants.DEFAULT_ADDR, constants.DEFAULT_PORT))
        except socket.error:
            self.fail("No se pudo establecer conexión al server")
        s.send('quit\r\n'.encode("ascii"))
        # Le damos TIMEOUT segundos para responder _algo_ y desconectar
        w, _, __ = select.select([s], [], [], TIMEOUT)
        self.assertEqual(
            w, [s],
            "Se envió quit, no hubo respuesta en %0.1f segundos" % TIMEOUT)
        # Medio segundo más par
        start = time.process_time()
        got = s.recv(1024)
        while got and time.process_time() - start <= 0.5:
            r, w, e = select.select([s], [], [], 0.5)
            self.assertEqual(
                r, [s],
                "Luego de la respuesta de quit, la "
                "conexión se mantuvo activa por más "
                "de 0.5 segundos")
            got = s.recv(1024)
        # Se desconectó?
        self.assertTrue(not got)
        s.close()

    def test_quit_answers_ok(self):
        c = self.new_client()
        c.close()
        self.assertEqual(c.status, constants.CODE_OK)

    def test_lookup(self):
        # Preparar el directorio con datos
        f = open(os.path.join(DATADIR, 'bar'), 'w').close()
        f = open(os.path.join(DATADIR, 'foo'), 'w').close()
        f = open(os.path.join(DATADIR, 'x'), 'w').close()
        c = self.new_client()
        files = sorted(c.file_lookup())
        self.assertEqual(c.status, constants.CODE_OK)
        # La lista de archivos es la correcta?
        self.assertEqual(files, ['bar', 'foo', 'x'])
        c.close()

    def test_get_metadata(self):
        test_size = 123459
        f = open(os.path.join(DATADIR, 'bar'), 'w')
        f.write('x' * test_size)
        f.close()
        c = self.new_client()
        m = c.get_metadata('bar')
        self.assertEqual(c.status, constants.CODE_OK)
        self.assertEqual(
            m, test_size,
            "El tamaño reportado para el archivo no es el correcto")
        c.close()

    def test_get_metadata_empty(self):
        f = open(os.path.join(DATADIR, 'bar'), 'w').close()
        c = self.new_client()
        m = c.get_metadata('bar')
        self.assertEqual(c.status, constants.CODE_OK)
        self.assertEqual(
            m, 0,
            "El tamaño reportado para el archivo no es el correcto")
        c.close()

    def test_get_full_slice(self):
        self.output_file = 'bar'
        test_data = 'The quick brown fox jumped over the lazy dog'
        f = open(os.path.join(DATADIR, self.output_file), 'w')
        f.write(test_data)
        f.close()
        c = self.new_client()
        c.get_slice(self.output_file, 0, len(test_data))
        self.assertEqual(c.status, constants.CODE_OK)
        f = open(self.output_file)
        self.assertEqual(
            f.read(), test_data,
            "El contenido del archivo no es el correcto")
        f.close()
        c.close()

    def test_partial_slices(self):
        self.output_file = 'bar'
        test_data = 'a' * 100 + 'b' * 200 + 'c' * 300
        f = open(os.path.join(DATADIR, self.output_file), 'w')
        f.write(test_data)
        f.close()
        c = self.new_client()
        c.get_slice(self.output_file, 0, 100)
        self.assertEqual(c.status, constants.CODE_OK)
        f = open(self.output_file)
        self.assertEqual(
            f.read(), 'a' * 100,
            "El contenido del archivo no es el correcto")
        f.close()
        c.get_slice(self.output_file, 100, 200)
        self.assertEqual(c.status, constants.CODE_OK)
        f = open(self.output_file)
        self.assertEqual(
            f.read(),
            'b' * 200, "El contenido del archivo no es el correcto")
        f.close()
        c.get_slice(self.output_file, 200, 200)
        self.assertEqual(c.status, constants.CODE_OK)
        f = open(self.output_file)
        self.assertEqual(
            f.read(),
            'b' * 100 + 'c' * 100,
            "El contenido del archivo no es el correcto")
        f.close()
        c.get_slice(self.output_file, 500, 100)
        self.assertEqual(c.status, constants.CODE_OK)
        f = open(self.output_file)
        self.assertEqual(
            f.read(),
            'c' * 100, "El contenido del archivo no es el correcto")
        f.close()
        c.close()


def main():
    pass


if __name__ == '__main__':
    main()
