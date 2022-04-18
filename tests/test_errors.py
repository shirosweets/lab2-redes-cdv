import os
import constants

from tests.test_base import TIMEOUT
from tests.test_base import DATADIR
from tests.test_base import TestBase


class TestHFTPErrors(TestBase):

    def test_bad_eol(self):
        c = self.new_client()
        c.send('qui\nt\n')
        status, message = c.read_response_line(TIMEOUT)
        self.assertEqual(
            status, constants.BAD_EOL,
            "El servidor no contestó 100 ante un fin de línea erróneo")

    def test_bad_command(self):
        c = self.new_client()
        c.send('verdura')
        status, message = c.read_response_line(TIMEOUT)
        self.assertEqual(
            status, constants.INVALID_COMMAND,
            "El servidor no contestó 200 ante un comando inválido")
        c.close()

    def test_bad_argument_count(self):
        c = self.new_client()
        c.send('quit passing extra arguments!')
        status, message = c.read_response_line(TIMEOUT)
        self.assertEqual(
            status, constants.INVALID_ARGUMENTS,
            "El servidor no contestó 201 ante una lista de argumentos "
            "muy larga")
        c.close()

    def test_bad_argument_count_2(self):
        c = self.new_client()
        c.send('get_metadata')  # Sin argumentos
        status, message = c.read_response_line(TIMEOUT)
        self.assertEqual(
            status, constants.INVALID_ARGUMENTS,
            "El servidor no contestó 201 ante una lista de argumentos "
            "muy corta")
        c.close()

    def test_bad_argument_type(self):
        f = open(os.path.join(DATADIR, 'bar'), 'w')
        f.write('data')
        f.close()
        c = self.new_client()
        c.send('get_slice bar x x')  # Los argumentos deberían ser enteros
        status, message = c.read_response_line(TIMEOUT)
        self.assertEqual(
            status, constants.INVALID_ARGUMENTS,
            "El servidor no contestó 201 ante una lista de argumentos "
            "mal tipada (status=%d)" % status)
        c.close()

    def test_file_not_found(self):
        c = self.new_client()
        c.send('get_metadata does_not_exist')
        status, message = c.read_response_line(TIMEOUT)
        self.assertEqual(
            status, constants.FILE_NOT_FOUND,
            "El servidor no contestó 202 ante un archivo inexistente")
        c.close()
