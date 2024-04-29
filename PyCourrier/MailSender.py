import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from contextlib import AbstractContextManager

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

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def __str__(self):
        return f"MailSender connected to {self.server_name}:{self.server_port}, Connected: {self.connected}"

    def set_message(self, in_plaintext="", in_subject="", in_from=None, in_htmltext=None, attachment=None, filename=None):
        """
        Compose an email message.

        :param in_plaintext: Plain text email body (required if no HTML text is provided)
        :param in_subject: Subject line
        :param in_from: Sender address
        :param in_htmltext: HTML version of the email body
        :param attachment: Path to attachment file
        :param filename: Filename for the attachment
        """
        self.msg = MIMEMultipart('alternative')

        if in_htmltext:
            self.msg.attach(MIMEText(in_htmltext, 'html'))
        if in_plaintext:
            self.msg.attach(MIMEText(in_plaintext, 'plain'))

        self.msg['Subject'] = in_subject
        self.msg['From'] = in_from or self.username

        # Include an attachment if specified
        if attachment:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(attachment, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename={filename}")
            self.msg.attach(part)

    def set_recipients(self, in_recipients):
        """
        Set the recipients for the email.

        :param in_recipients: List of recipient email addresses
        """
        if isinstance(in_recipients, (list, tuple)):
            self.recipients = in_recipients
        else:
            raise TypeError("Recipients must be a list or tuple")

    def add_recipient(self, in_recipient):
        """Add a recipient to the list of recipients."""
        self.recipients.append(in_recipient)

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
            print(f"Connected to {self.server_name}")
        except (smtplib.SMTPException, ConnectionError) as error:
            self.connected = False
            raise ConnectionError(f"Failed to connect to {self.server_name}: {error}")


    def disconnect(self):
        """Disconnect from the SMTP server."""
        if self.smtpserver:
            self.smtpserver.quit()
            self.connected = False

    def send_all(self, close_connection=True):
        """Send the email to all recipients."""
        if not self.connected:
            raise ConnectionError("Not connected to any server. Please connect first.")

        for recipient in self.recipients:
            self.msg['To'] = recipient 
            print(f"Sending to {recipient}")

            # Convert the message to a string and then send it
            self.smtpserver.sendmail(self.username, recipient, self.msg.as_string())

        print("All messages sent")

