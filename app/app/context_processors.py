from django.conf import settings

from core.models import MetaTag


def app_settings(request):
    return {'settings': {
        'EMAIL_ADMIN_ADDRESS': settings.EMAIL_ADMIN_ADDRESS,
        'MAIN_PHONE': settings.MAIN_PHONE,
        'MAIN_PHONE_RAW': settings.MAIN_PHONE_RAW,
        'FACT_ADDRESS': settings.FACT_ADDRESS,
        'YANDEX_MAPS_LINK': settings.YANDEX_MAPS_LINK,
        'YANDEX_MAPS_API_LINK': settings.YANDEX_MAPS_API_LINK,
    }}


def meta_tags(request):
    return {'meta_tags': MetaTag.objects.all()}
