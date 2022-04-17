import os
import constants

from tests.test_base import TIMEOUT
from tests.test_base import DATADIR
from tests.test_base import TestBase

class TestHFTPHard(TestBase):

    def test_multiple_commands(self):
        client = self.new_client()
        socket_message_len = client.s.send(
            'get_file_listing\r\nget_file_listing\r\n'.encode("ascii"))
        assert socket_message_len == len(
            'get_file_listing\r\nget_file_listing\r\n'.encode("ascii"))
        status, message = client.read_response_line(TIMEOUT)
        self.assertEqual(
            status, constants.CODE_OK,
            "El servidor no entendio muchos mensajes correctos "
            "enviados juntos")
        client.connected = False
        client.s.close()

    def test_data_with_nulls(self):
        self.output_file = 'bar'
        test_data = 'x' * 100 + '\0' * 100 + 'y' * 100
        f = open(os.path.join(DATADIR, self.output_file), 'w')
        f.write(test_data)
        f.close()
        c = self.new_client()
        c.get_slice(self.output_file, 0, len(test_data))
        self.assertEqual(c.status, constants.CODE_OK)
        f = open(self.output_file)
        self.assertEqual(
            f.read(), test_data,
            "El contenido del archivo con NULs no es el correcto")
        f.close()
        c.close()

    def test_long_file_listing(self):
        # Preparar el directorio de datos
        correct_list = []
        for i in range(1000):
            filename = 'test_file%04d' % i
            f = open(os.path.join(DATADIR, filename), 'w').close()
            correct_list.append(filename)
        c = self.new_client()
        files = sorted(c.file_lookup())
        self.assertEqual(c.status, constants.CODE_OK)
        self.assertEqual(
            files, correct_list,
            "La lista de 1000 archivos no es la correcta")
        c.close()

def main():
    pass

if __name__ == '__main__':
    main()
