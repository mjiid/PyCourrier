from email.header import Header
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from contextlib import AbstractContextManager
import logging
from asyncio import gather, to_thread
from typing import List, Tuple, Optional, Dict, Union
import os
import ssl
from email.utils import formataddr

from .config import EMAIL_SERVICES
from .exceptions import ConnectionError, MessageError
from .utils import attach_file, validate_email

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MailSender(AbstractContextManager):
    """
    A class that facilitates composing and sending emails via SMTP.

    :param in_username: Username for mail server login
    :param in_password: Password for mail server login
    :param in_service: Name of the email service provider (e.g., 'gmail')
    :param use_SSL: Use SSL (True) or TLS (False, default) for connection
    """
    def __init__(self, in_username: str, in_password: str, 
                 in_service: str = 'gmail', use_SSL: bool = False):
        if in_service not in EMAIL_SERVICES:
            raise ValueError(f"Unsupported email service: {in_service}")
        self.username = in_username
        self.password = in_password
        self.server_name, self.server_port = EMAIL_SERVICES[in_service]
        self.use_SSL = use_SSL
        self.smtpserver: Optional[smtplib.SMTP] = None
        self.connected = False
        self.recipients: List[str] = []
        self.cc_recipients: List[str] = []
        self.bcc_recipients: List[str] = []
        self.attachments: List[Dict[str, str]] = []
        self.inline_images: List[Dict[str, str]] = []
        self.msg: Optional[MIMEMultipart] = None

    async def __aenter__(self):
        await to_thread(self.connect)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await to_thread(self.disconnect)

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
            logging.info(f"Connected to {self.server_name} on port {self.server_port}")
        except (smtplib.SMTPException, ConnectionError) as error:
            self.connected = False
            logging.error(f"Failed to connect to {self.server_name}: {error}")
            raise ConnectionError(f"Failed to connect to {self.server_name}: {error}")

    def disconnect(self):
        """Disconnect from the SMTP server."""
        if self.smtpserver:
            try:
                self.smtpserver.quit()
                logging.info("Disconnected from the SMTP server.")
            except smtplib.SMTPException as e:
                logging.warning(f"Error disconnecting from SMTP server: {e}")
            finally:
                self.connected = False

    def set_message(self, in_subject: str = "", in_from: Optional[str] = None, 
                    in_plaintext: Optional[str] = None, in_htmltext: Optional[str] = None):
        """
        Compose an email message.

        :param in_plaintext: Plain text email body (required if no HTML text is provided)
        :param in_subject: Subject line
        :param in_from: Sender address
        :param in_htmltext: HTML version of the email body
        """
        if not (in_plaintext or in_htmltext):
            raise MessageError("Either plaintext or HTML text must be provided for the email body.")

        self.msg = MIMEMultipart('alternative')
        self.msg['Subject'] = in_subject
        self.msg['From'] = formataddr((str(Header(in_from or self.username, 'utf-8')), self.username))

        if in_plaintext:
            part1 = MIMEText(in_plaintext, 'plain')
            self.msg.attach(part1)
        if in_htmltext:
            part2 = MIMEText(in_htmltext, 'html')
            self.msg.attach(part2)

    def add_attachment(self, path: str, filename: str):
        """Add an attachment."""
        self.attachments.append({'path': path, 'filename': filename})
        logging.info(f"Attachment added: {filename}")

    def add_inline_image(self, path: str, cid: str, filename: str):
        """Add an inline image."""
        self.inline_images.append({'path': path, 'cid': cid, 'filename': filename})
        logging.info(f"Inline image added with CID: {cid}, filename: {filename}")

    def set_recipients(self, in_recipients: Union[List[str], Tuple[str, ...]], 
                       cc_recipients: Optional[Union[List[str], Tuple[str, ...]]] = None, 
                       bcc_recipients: Optional[Union[List[str], Tuple[str, ...]]] = None):
        """
        Set the recipients for the email.

        :param in_recipients: List of recipient email addresses
        :param cc_recipients: List of CC recipient email addresses
        :param bcc_recipients: List of BCC recipient email addresses
        """
        self._set_recipient_list(in_recipients, 'recipients')
        self._set_recipient_list(cc_recipients, 'cc_recipients')
        self._set_recipient_list(bcc_recipients, 'bcc_recipients')
            
    def _set_recipient_list(self, recipients: Optional[Union[List[str], Tuple[str, ...]]], attr_name: str):
        if recipients:
            if isinstance(recipients, (list, tuple)):
                setattr(self, attr_name, [addr for addr in recipients if validate_email(addr)])
                logger.info(f"{attr_name.capitalize()} set: {', '.join(getattr(self, attr_name))}")
            else:
                logger.error(f"{attr_name.capitalize()} must be a list or tuple")
                raise TypeError(f"{attr_name.capitalize()} must be a list or tuple")

    async def send_all_async(self):
        """Send the email to all recipients."""
        if not self.connected:
            logging.error("Not connected to any server. Please connect first.")
            raise ConnectionError("Not connected to any server. Please connect first.")

        if not self.msg:
            logging.error("Message not set. Please set the message before sending.")
            raise MessageError("Message not set.")

        all_recipients = self.recipients + self.cc_recipients + self.bcc_recipients
        tasks = [self.send_email(recipient) for recipient in all_recipients]
        await gather(*tasks)
        logging.info("All messages sent")

    async def send_email(self, recipient: str):
        """Send the email to a single recipient."""
        try:
            logging.info(f"Sending to {recipient}")

            # Create a new message for each recipient to set the 'To', 'CC', and 'BCC' headers individually
            msg = MIMEMultipart('alternative')
            msg['Subject'] = self.msg['Subject']
            msg['From'] = self.msg['From']
            msg['To'] = recipient
            msg['CC'] = ', '.join(self.cc_recipients) if self.cc_recipients else ''
            msg['BCC'] = ', '.join(self.bcc_recipients) if self.bcc_recipients else ''

            # Attach the plain and HTML parts from the original message
            for part in self.msg.get_payload():
                msg.attach(part)
            
            # Attach inline images
            for image in self.inline_images:
                with open(image['path'], 'rb') as img:
                    mime_image = MIMEImage(img.read(), name=os.path.basename(image['filename']))
                    mime_image.add_header('Content-ID', f"<{image['cid']}>")
                    mime_image.add_header('Content-Disposition', 'inline', filename=image['filename'])
                    msg.attach(mime_image)

            # Attach any files
            for attachment in self.attachments:
                attach_file(msg, attachment['path'], attachment['filename'])

            # Convert the message to a string and then send it
            self.smtpserver.sendmail(self.username, [recipient] + self.cc_recipients + self.bcc_recipients, msg.as_string())
            logging.info(f"Mail sent to {recipient}")
        except smtplib.SMTPException as error:
            logging.error(f"Failed to send mail to {recipient}: {error}")
            raise
