from django.contrib import admin

from log_cats.models import ExtraService, DeliveryType


@admin.register(ExtraService)
class ExtraServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(DeliveryType)
class DeliveryTypeAdmin(admin.ModelAdmin):
    pass
