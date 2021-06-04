import sendgrid
import requests

from sendgrid.helpers.mail import *
from st2common.runners.base_action import Action

__all__ = [
    'SendEmailAction'
]

class SendEmailAction(Action):
    def run(self, sender, recipient, subject, content_type, content_value):
        api_key = self.config['api_key']
        sg = sendgrid.SendGridAPIClient(api_key=api_key)
        from_email = Email(sender)
        to_email = To(recipient)
        subject = subject
        content = Content(content_type, content_value)
        mail = Mail(from_email, to_email, subject, content)
        response = sg.client.mail.send.post(request_body=mail.get())

        if response.status_code != requests.codes.ok:  # pylint: disable=no-member
            msg = ('Failed to send message (status_code=%s): %s' %
                   (response.status_code, response.text))
            raise Exception(msg)

        return True
