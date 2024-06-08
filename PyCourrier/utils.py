from email.mime.base import MIMEBase
from email import encoders
import logging

def attach_file(msg, path: str, filename: str):
    """Attach a file to the email message."""
    try:
        with open(path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={filename}')
            msg.attach(part)
    except IOError as e:
        logging.error(f"Failed to attach file {path}: {e}")
        raise
