import os
import constants

from tests.test_base import TIMEOUT
from tests.test_base import TestBase


class TestHFTPCommandInPieces(TestBase):
    def test_command_in_pieces(self):
        c = self.new_client()
        for ch in 'quit\r\n':
            c.s.send(ch.encode("ascii"))
            os.system('sleep 1')  # Despaciiiiiiiiiiito
        status, message = c.read_response_line(TIMEOUT)
        self.assertEqual(
            status, constants.CODE_OK,
            "El servidor no entendio un quit enviado de a un caracter por vez")


def main():
    pass


if __name__ == '__main__':
    main()
