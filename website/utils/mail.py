from flask_mailman import EmailMessage

from flask import current_app
#from website import mail


def send_confirm_email(to, subject, template):
    msg = EmailMessage(
        subject,
        template,
        're.click@outlook.com',
        [to]
    )
    msg.content_subtype = 'html'
    msg.send()