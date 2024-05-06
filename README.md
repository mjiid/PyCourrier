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
from asyncio import run

async def main():
    # Create a MailSender instance within a context manager
    with MailSender('your_email@gmail.com', 'your_generated_app_password') as sender:

        # Set recipients
        recipients = ['recipient1@gmail.com', 'recipient2@gmail.com', 'recipient3@gmail.com']
        sender.set_recipients(recipients)

        # Set email message details
        in_subject='Hello from PyCourrier!'
        in_plaintext='This is the plain text content of the email.'
        in_htmltext='<p>This is the HTML content of the email.</p> (optional)'

        # Add attachments (optional)
        sender.add_attachment('path/to/attachment', 'filename')

        # set the message
        sender.set_message(in_plaintext=in_plaintext, in_subject=in_subject, in_htmltext=in_htmltext)
        await sender.send_all_async()


# Run the async main function
if __name__ == "__main__":
    run(main())

```

## Parameters:
- **in_username**: Your email address used for SMTP login.
- **in_password**: Your generated app password for SMTP login.
- **in_server**: Tuple containing the SMTP server address and port (default is Gmail).
- **use_SSL**: Boolean indicating whether to use SSL (True) or TLS (False, default) for the connection.

## Methods:
- **set_message**: Compose the email message with subject, plaintext, and HTML content.
- **add_attachment**: Add an attachment to the email.
- **set_recipients**: Set the list of email recipients.
- **connect**: Connect to the SMTP server.
- **disconnect**: Disconnect from the SMTP server.
- **send_all_async**: Send the composed email to all recipients asynchronously.
- **send_email**: Send the composed email to a specific recipient.

## Contribution
Contributions to PyCourrier are welcome! If you encounter any issues or have suggestions for improvements, please open an [issue on GitHub](https://github.com/mjiid/PyCourrier/issues).

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.