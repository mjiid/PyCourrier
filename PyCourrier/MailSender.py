import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from contextlib import AbstractContextManager
import logging
from asyncio import gather


# Setup logging
logging.basicConfig(level=logging.DEBUG)

class MailSender(AbstractContextManager):
    """
    A class that facilitates composing and sending emails via SMTP.

    :param in_username: Username for mail server login
    :param in_password: Password for mail server login
    :param in_server: SMTP server to connect to (default is Gmail)
    :param use_SSL: Use SSL (True) or TLS (False, default) for connection
    """
    def __init__(self, in_username, in_password, in_server=("smtp.gmail.com", 587), use_SSL=False):
        self.username = in_username
        self.password = in_password
        self.server_name, self.server_port = in_server
        self.use_SSL = use_SSL
        self.smtpserver = None
        self.connected = False
        self.recipients = []
        self.attachments = []
        self.msg = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        """Connect to the SMTP server."""
        try:
            if self.use_SSL:
                self.smtpserver = smtplib.SMTP_SSL(self.server_name, self.server_port)
            else:
                self.smtpserver = smtplib.SMTP(self.server_name, self.server_port)
                self.smtpserver.starttls()

            self.smtpserver.login(self.username, self.password)
            self.connected = True
            logging.info(f"Connected to {self.server_name}")
        except (smtplib.SMTPException, ConnectionError) as error:
            self.connected = False
            logging.error(f"Failed to connect to {self.server_name}: {error}")
            raise ConnectionError(f"Failed to connect to {self.server_name}: {error}")

    def disconnect(self):
        """Disconnect from the SMTP server."""
        if self.smtpserver:
            try:
                self.smtpserver.quit()
            except Exception as e:
                logging.warning(f"Error disconnecting from SMTP server: {e}")
            finally:
                self.connected = False
                logging.info("Disconnected.")

    def set_message(self, in_subject="", in_from=None, in_plaintext=None, in_htmltext=None):
        """
        Compose an email message.

        :param in_plaintext: Plain text email body (required if no HTML text is provided)
        :param in_subject: Subject line
        :param in_from: Sender address
        :param in_htmltext: HTML version of the email body
        """
        self.msg = MIMEMultipart('alternative')
        self.msg['Subject'] = in_subject
        self.msg['From'] = in_from or self.username

        if in_plaintext:
            self.msg.attach(MIMEText(in_plaintext, 'plain'))
        if in_htmltext:
            self.msg.attach(MIMEText(in_htmltext, 'html'))

        # Include an attachment if specified
        for attachment in self.attachments:
            try:
                with open(attachment['path'], 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition', 
                        f'attachment; filename={attachment["filename"]}'
                    )
                    self.msg.attach(part)
            except IOError as e:
                logging.error(f"Failed to attach file {attachment['path']}: {e}")
                raise

    def add_attachment(self, path, filename):
        """Add an attachment"""
        self.attachments.append({'path': path, 'filename': filename})

    def set_recipients(self, in_recipients):
        """
        Set the recipients for the email.

        :param in_recipients: List of recipient email addresses
        """
        if isinstance(in_recipients, (list, tuple)):
            self.recipients = in_recipients
        else:
            logging.error("Recipients must be a list or tuple")
            raise TypeError("Recipients must be a list or tuple")

    async def send_all_async(self):
        """Send the email to all recipients."""
        if not self.connected:
            logging.error("Not connected to any server. Please connect first.")
            raise ConnectionError("Not connected to any server. Please connect first.")

        if not self.msg:
            logging.error("Message not set. Please set the message before sending.")
            raise ValueError("Message not set.")

        tasks = [self.send_email(recipient) for recipient in self.recipients]
        await gather(*tasks)
        logging.info("All messages sent")

    async def send_email(self, recipient):
        """Send the email to a single recipient."""
        try:
            logging.info(f"Sending to {recipient}")

            # Create a new message for each recipient to set the 'To' header individually
            msg = MIMEMultipart('alternative')
            msg['Subject'] = self.msg['Subject']
            msg['From'] = self.msg['From']
            msg['To'] = recipient  # Set the recipient's email

            # Attach the plain and HTML parts from the original message
            for part in self.msg.get_payload():
                msg.attach(part)

            # Convert the message to a string and then send it
            self.smtpserver.sendmail(self.username, recipient, msg.as_string())
        except smtplib.SMTPException as error:
            logging.error(f"Failed to send mail to {recipient}: {error}")
            raise

