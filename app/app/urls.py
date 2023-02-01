from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('docs/', include('dynamic_docs.urls')),
    path('order/', include('logistics.urls')),
    path('auth/', include('app_auth.urls')),
    path('clientsarea/', include('clients_area.urls')),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico')))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
