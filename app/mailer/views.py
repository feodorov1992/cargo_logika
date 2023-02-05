from smtplib import SMTPRecipientsRefused

from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from django.contrib.staticfiles import finders
from functools import lru_cache


@lru_cache()
def logo_data():
    with open(finders.find('img/logo_color.png'), 'rb') as f:
        logo_data = f.read()
    logo = MIMEImage(logo_data)
    logo.add_header('Content-ID', '<logo>')
    return logo


def send_logo_mail(subject, body_text, body_html, from_email, recipients, **kwargs):
    message = EmailMultiAlternatives(
        subject=subject,
        body=body_text,
        from_email=from_email,
        to=recipients,
        **kwargs
    )
    message.mixed_subtype = 'related'
    message.attach_alternative(body_html, "text/html")
    message.attach(logo_data())

    try:
        return message.send(fail_silently=False)
    except SMTPRecipientsRefused:
        return 0
