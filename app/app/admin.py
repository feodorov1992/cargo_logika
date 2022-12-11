from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class CargoLogikaAdminSite(admin.AdminSite):
    site_header = _('Cargo Logika management')
    site_title = _('Cargo Logika')
