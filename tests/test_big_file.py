import os
import constants

from tests.test_base import DATADIR
from tests.test_base import TestBase


class TestHFTPBigFile(TestBase):
    print("TestHFTPBigFile()")
    # def test_big_file(self):
    #     self.output_file = 'bar'
    #     f = open(os.path.join(DATADIR, self.output_file), 'wb')
    #     for i in range(1, 255):
    #         f.write(bytes([i]) * (2 ** 17))  # 128KB
    #     f.close()

    #     c = self.new_client()
    #     size = c.get_metadata(self.output_file)
    #     self.assertEqual(c.status, constants.CODE_OK)
    #     c.get_slice(self.output_file, 0, size)
    #     self.assertEqual(c.status, constants.CODE_OK)
    #     f = open(self.output_file, "rb")
    #     for i in range(1, 255):
    #         s = f.read(2 ** 17)  # 128 KB
    #         self.assertEqual(
    #             s, bytes([i]) * (2 ** 17),
    #             "El contenido del archivo no es el correcto")
    #     f.close()
    #     c.close()


def main():
    pass

if __name__ == '__main__':
    main()
