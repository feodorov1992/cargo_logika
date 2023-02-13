from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from mailer.views import send_model_email


CP_TYPES = (
    ('individual', _('Individual')),
    ('company', _('Company'))
)


class User(AbstractUser):
    org_name = models.CharField(max_length=255, verbose_name=_('Organisation name'), blank=True, null=True)
    tin = models.CharField(max_length=15, verbose_name=_('User TIN'), blank=True, null=True)
    contract = models.CharField(max_length=255, verbose_name=_('Contract number'), blank=True, null=True)

    def send_creation_email(self):
        subject = _('New user has been registered')
        from_email = 'register@cargo-logika.ru'

        template_name = 'app_auth/mail/new_user'
        recipients = [settings.EMAIL_ADMIN_ADDRESS]

        return send_model_email.delay(subject, template_name, 'app_auth.models.User', self.pk, from_email, recipients)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
