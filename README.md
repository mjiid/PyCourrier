# PyCourrier

PyCourrier is a Python package that simplifies composing and sending emails using SMTP. This package allows you to connect to an SMTP server, set up email content (including plain text, HTML, and attachments), specify recipients, and send emails seamlessly.

## Features

- Connect to SMTP servers (supports both SSL and TLS connections).
- Compose emails with plaintext, HTML, and attachments.
- Set multiple recipients for each email.
- Easily send emails to all recipients with a single function call.

## Installation

You can install PyCourrier using pip:

```bash
pip install PyCourrier
```

## Usage

Here's a quick guide on how to use MailSender:

```python
from PyCourrier import MailSender

# Create a MailSender instance within a context manager
with MailSender('your_email@gmail.com', 'your_generated_app_password') as mailSender:

    # Set recipients
    recipients = ['Abdelmajiid.habouch@gmail.com']
    mail_sender.set_recipients(recipients)

    # Set email message details
    in_subject='Hello from PyCourrier!',
    in_plaintext='This is the plain text content of the email.',
    in_from='your_email@gmail.com (optioanl)',
    in_htmltext='<p>This is the HTML content of the email.</p> (optional)',
    attachment="path/to/file (optional)",
    filename="filename_for_the_attachment (optional)"

    mail_sender.set_message(in_plaintext=plaintext_body, in_subject=in_subject, in_from=in_from, in_htmltext=in_htmltext, attachment=attachment, filename=filename)

    # Send the email to all recipients
    mail_sender.send_all()
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
Contributions to PyCourrier are welcome! If you encounter any issues or have suggestions for improvements, please open an [issue on GitHub](https://github.com/mjiid/PyCourrier/issues).

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.