from django.db import models
from django.utils.translation import gettext_lazy as _


class Sample(models.Model):
    attachment = models.FileField(verbose_name=_('attachment'))

    class Meta:
        verbose_name = _('sample')
        verbose_name_plural = _('samples')
