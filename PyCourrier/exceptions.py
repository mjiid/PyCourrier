class MailSenderError(Exception):
    """Base class for exceptions in MailSender."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class ConnectionError(MailSenderError):
    """Raised when connection to the SMTP server fails."""
    def __init__(self, message: str = "Failed to connect to the SMTP server"):
        super().__init__(message)


class MessageError(MailSenderError):
    """Raised when there's an error with the email message."""
    def __init__(self, message: str = "Error with the email message"):
        super().__init__(message)
