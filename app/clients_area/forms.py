from django import forms
from django.utils.translation import gettext_lazy as _
from logistics.models import Order


class ClientsAreaOrdersFilters(forms.Form):
    order_date__gte = forms.DateField(label=_('Not earlier'), required=False,
                                      widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'))
    order_date__lte = forms.DateField(label=_('Not later'), required=False,
                                      widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'))
