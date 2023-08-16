from django.db import models
from django.utils.translation import gettext_lazy as _


class Document(models.Model):
    label = models.CharField(max_length=50, verbose_name=_('label'))
    file = models.FileField(upload_to='docs/', verbose_name=_('file'))

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')


class PhotoBlock(models.Model):
    ordering_num = models.IntegerField(verbose_name=_('ordering_num'), default=0)
    title = models.CharField(verbose_name=_('title'), max_length=255)
    text = models.TextField(verbose_name=_('text'))
    img = models.ImageField(verbose_name=_('photo'), upload_to='main_photos/')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['ordering_num', 'id']
        verbose_name = _('photo block')
        verbose_name_plural = _('photo blocks')


class IconBlock(models.Model):
    ordering_num = models.IntegerField(verbose_name=_('ordering_num'), default=0)
    title = models.CharField(verbose_name=_('title'), max_length=255)
    text = models.CharField(verbose_name=_('text'), max_length=255)
    img = models.FileField(verbose_name=_('icon'), upload_to='main_icons/')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['ordering_num', 'id']
        verbose_name = _('icon block')
        verbose_name_plural = _('icon blocks')


class MetaTag(models.Model):
    name = models.CharField(max_length=30)
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('meta tag')
        verbose_name_plural = _('meta tags')
