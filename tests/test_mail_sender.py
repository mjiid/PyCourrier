import unittest
from PyCourrier import MailSender, ConnectionError, MessageError

class TestMailSender(unittest.TestCase):

    def test_invalid_service(self):
        with self.assertRaises(ValueError):
            MailSender('username', 'password', 'invalid_service')

    def test_connect(self):
        mail_sender = MailSender('username', 'password', 'gmail')
        with self.assertRaises(ConnectionError):
            mail_sender.connect()

    def test_set_message(self):
        mail_sender = MailSender('username', 'password', 'gmail')
        mail_sender.set_message('Test Subject', 'sender@example.com', 'This is a test.')
        self.assertIsNotNone(mail_sender.msg)

    def test_add_attachment(self):
        mail_sender = MailSender('username', 'password', 'gmail')
        mail_sender.add_attachment('path/to/file', 'filename')
        self.assertEqual(len(mail_sender.attachments), 1)

    def test_set_recipients(self):
        mail_sender = MailSender('username', 'password', 'gmail')
        mail_sender.set_recipients(['recipient1@example.com', 'recipient2@example.com'])
        self.assertEqual(len(mail_sender.recipients), 2)


if __name__ == '__main__':
    unittest.main()
