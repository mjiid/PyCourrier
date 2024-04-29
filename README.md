# PyCourrier

PyCourrier is a Python package that simplifies composing and sending emails using SMTP. This package allows you to connect to an SMTP server, set up email content (including plain text, HTML, and attachments), specify recipients, and send emails seamlessly.

## Features

- Connect to SMTP servers (supports both SSL and TLS connections).
- Compose emails with plaintext, HTML, and attachments.
- Set multiple recipients for each email.
- Easily send emails to all recipients with a single function call.

## Installation

You can install pycourrier using pip:

```bash
pip install pycourrier
```

## Usage

Here's a quick guide on how to use MailSender:

```python
from pycourrier import MailSender

# Initialize MailSender with your SMTP server credentials
mailer = MailSender(in_username='your_email@gmail.com', in_password='your_password')

# Set email message content
mailer.set_message(
    in_subject='Hello from MailSender!',
    in_plaintext='This is the plain text content of the email.',
    in_from='your_email@gmail.com',
    in_htmltext='<p>This is the HTML content of the email.</p>'
)

# Add recipients
mailer.set_recipients(['recipient1@example.com', 'recipient2@example.com'])

# Send the email to all recipients
mailer.connect()  # Connect to the SMTP server
mailer.send_all()  # Send the email and disconnect
```

## Constructor Parameters
- **in_username**: Your email address used for SMTP login.
- **in_password**: Your Generated app password.
- **in_server**: Tuple containing the SMTP server address and port (default is Gmail).
- **use_SSL**: Boolean indicating whether to use SSL (True) or TLS (False, default) for the connection.
Methods
- **set_message**: Compose the email message with subject, plaintext, HTML content, and optional attachments.
- **set_recipients**: Set the list of email recipients.
- **add_recipient**: Add a single recipient to the list of recipients.
- **connect**: Connect to the SMTP server.
- **disconnect**: Disconnect from the SMTP server.
- **send_all**: Send the composed email to all recipients.

## Contribution
Contributions to pycourrier are welcome! If you encounter any issues or have suggestions for improvements, please open an [issue on GitHub](https://github.com/mjiid/pycourrier/issues).

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.