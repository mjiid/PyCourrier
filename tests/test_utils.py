import unittest
from email.mime.multipart import MIMEMultipart
from PyCourrier.utils import attach_file

class TestUtils(unittest.TestCase):

    def test_attach_file(self):
        msg = MIMEMultipart()
        attach_file(msg, 'path/to/file', 'filename')
        self.assertEqual(len(msg.get_payload()), 1)


if __name__ == '__main__':
    unittest.main()
