import os.path
from django import template
from app import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def static(context, path):
    full_path = os.path.join(settings.STATIC_ROOT, os.path.normpath(path))
    return 'file://' + full_path


@register.simple_tag(takes_context=True)
def media(context, path):
    full_path = os.path.join(settings.MEDIA_ROOT, os.path.normpath(path))
    return 'file://' + full_path
