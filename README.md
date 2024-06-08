# PyCourrier

PyCourrier is a Python package for sending emails using various SMTP services.

## Features

- Support for multiple email services (Gmail, Yahoo, Outlook, etc.) (Check the `config.py` file for more details)
- Easy to use context manager for connecting and disconnecting from the SMTP server
- Support for plain text and HTML email bodies
- Attachment support
- Asynchronous email sending

## Installation

```bash
pip install PyCourrier
```

## Usage

Here's a quick guide on how to use MailSender:

```python
import asyncio
from PyCourrier import MailSender

async def main():
    # Initialize MailSender with your credentials and email service
    async with MailSender(in_username='your_email@example.com', 
                          in_password='your_app_password', 
                          in_service='gmail', 
                          use_SSL=True) as mail_sender:
        
        # Compose the email message
        mail_sender.set_message(
            in_subject='Test Email',
            in_from='your_email@example.com',
            in_plaintext='This is a test email with an attachment.',
            in_htmltext='<html><body><h1>This is a test email with an attachment.</h1></body></html>'
        )

        # Add attachments
        mail_sender.add_attachment(path='/path/to/your/file.txt', filename='file.txt')
        mail_sender.add_attachment(path='/path/to/another/file.pdf', filename='file.pdf')

        # Set recipients
        mail_sender.set_recipients(
            in_recipients=['recipient1@example.com', 'recipient2@example.com'],
            cc_recipients=['cc1@example.com'], # Optional (None by default)
            bcc_recipients=['bcc1@example.com'] # Optional (None by default)
        )

        # Send the email to all recipients
        await mail_sender.send_all_async()

# Run the main function
asyncio.run(main())

```

## Parameters:
- **in_username**: Your email address used for SMTP login.
- **in_password**: Your generated app password for SMTP login.
- **in_server**: Name of the email service provider (e.g., 'gmail', 'yahoo', 'outlook', or 'other'). Defaults to 'gmail'.
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