import asyncio
from PyCourrier import MailSender

async def main():
    # Initialize MailSender with your credentials and email service
    async with MailSender(in_username='your_email@example.com', 
                          in_password='your_password', 
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
            cc_recipients=['cc1@example.com'],
            bcc_recipients=['bcc1@example.com']
        )

        # Send the email to all recipients
        await mail_sender.send_all_async()

# Run the main function
asyncio.run(main())
