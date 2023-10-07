from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView

from app_auth.forms import UserLoginForm
from .sitemaps import StaticViewSitemap


sitemaps = {
    "static": StaticViewSitemap,
}

admin.autodiscover()
admin.site.login_form = UserLoginForm
admin.site.login_template = 'app_auth/admin_login.html'

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('docs/', include('dynamic_docs.urls')),
    path('order/', include('logistics.urls')),
    path('auth/', include('app_auth.urls')),
    path('clientsarea/', include('clients_area.urls')),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),
    path('robots.txt', TemplateView.as_view(template_name="core/robots.txt", content_type="text/plain")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    )
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
