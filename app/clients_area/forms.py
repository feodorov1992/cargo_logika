from django import forms
from django.utils.translation import gettext_lazy as _
from logistics.models import Order


class ClientsAreaOrdersFilters(forms.Form):
    order_date__gte = forms.DateField(label=_('Not earlier'), required=False,
                                      widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'))
    order_date__lte = forms.DateField(label=_('Not later'), required=False,
                                      widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'))
    delivery_date__gte = forms.DateField(label=_('Not earlier'), required=False,
                                         widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'))
    delivery_date__lte = forms.DateField(label=_('Not later'), required=False,
                                         widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'))

    def as_my_style(self):
        context = super().get_context()
        context['fields'] = {f_e[0].name: f_e[0] for f_e in context['fields']}
        context['hidden_fields'] = {f_e.name: f_e for f_e in context['hidden_fields']}
        return self.render(template_name='clients_area/basic_styles/order_filters_as_my_style.html', context=context)
