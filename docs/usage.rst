Usage
=====

Here is how you can use PyCourrier to send emails:

.. code-block:: python

    from PyCourrier import MailSender

    with MailSender('your_email@example.com', 'your_password', 'gmail') as mail_sender:
        mail_sender.set_recipients(['recipient@example.com'])
        mail_sender.set_message('Subject', 'your_email@example.com', 'This is the plain text body.')
        mail_sender.add_attachment('path/to/file', 'filename')
        mail_sender.send_all_async()

Refer to the API Reference for more details on the methods available.
