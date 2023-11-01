from smtplib import SMTPRecipientsRefused

from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from django.contrib.staticfiles import finders
from functools import lru_cache
from django.apps import apps
from django.template.loader import render_to_string
from app.celery import app


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


@app.task(bind=True)
def send_model_email(self, subject, template_name, model_path, obj_pk, from_email, recipients):
    app_label, _, class_name = model_path.split('.')
    model = apps.get_model(app_label, class_name)
    obj = model.objects.get(pk=obj_pk)
    body_text = render_to_string(f'{template_name}.txt', {'object': obj})
    body_html = render_to_string(f'{template_name}.html', {'object': obj})
    try:
        return send_logo_mail(subject, body_text, body_html, from_email, recipients)
    except ConnectionResetError as e:
        self.retry(exc=e, countdown=1.5)
