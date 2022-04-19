import constants

from tests.test_base import TIMEOUT
from tests.test_base import TestBase


class TestHFTPBigFileName(TestBase):
    def test_big_filename(self):
        c = self.new_client()
        c.send('get_metadata ' + 'x' * (5 * 2 ** 12), timeout=120)
        # Le damos 4 minutos a esto
        status, message = c.read_response_line(TIMEOUT * 6)
        # Le damos un rato mas
        self.assertEqual(
            status, constants.FILE_NOT_FOUND,
            "El servidor no contestó 202 ante un archivo inexistente con "
            "nombre muy largo (status=%d)" % status)
        c.close()


def main():
    pass


if __name__ == '__main__':
    main()
