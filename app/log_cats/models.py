from django.db import models
from django.utils.translation import gettext_lazy as _


class ExtraService(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('title'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('extra service')
        verbose_name_plural = _('extra services')


class DeliveryType(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('title'))

    @classmethod
    def get_default_pk(cls):
        if not cls.objects.exists():
            delivery_type = cls.objects.create(title=_('Auto'))
            return delivery_type.pk
        return cls.objects.first().pk

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('delivery type')
        verbose_name_plural = _('delivery types')
