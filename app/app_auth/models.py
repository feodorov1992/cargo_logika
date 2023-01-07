from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


CP_TYPES = (
    ('individual', _('Individual')),
    ('company', _('Company'))
)


class User(AbstractUser):
    org_name = models.CharField(max_length=255, verbose_name=_('Organisation name'), blank=True, null=True)
    type = models.CharField(max_length=15, verbose_name=_('User type'), choices=CP_TYPES,
                            default=CP_TYPES[0][0])
    tin = models.CharField(max_length=15, verbose_name=_('User TIN'), blank=True, null=True)
    passport = models.CharField(max_length=30, verbose_name=_('Payer passport'), blank=True, null=True)
    contract = models.CharField(max_length=255, verbose_name=_('Contract number'), blank=True, null=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
