from django.contrib import admin

from core.models import Document, PhotoBlock, IconBlock, MetaTag


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(PhotoBlock)
class PhotoBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'ordering_num')


@admin.register(IconBlock)
class IconBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'ordering_num')


@admin.register(MetaTag)
class MetaTagAdmin(admin.ModelAdmin):
    pass
