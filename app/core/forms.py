from django import forms
from django.template.defaultfilters import safe
from django.utils.translation import gettext_lazy as _
from logistics.models import LOADING_BY, UNLOADING_BY, PACKAGE_TYPES, ExtraService


class CalcForm(forms.Form):
    required_css_class = 'required'

    sub_phone = forms.CharField(label=_('Your phone'), widget=forms.TextInput(attrs={'type': 'tel'}), required=False)
    sub_email = forms.EmailField(label=_('Your E-mail'), required=False)
    sender_addr = forms.CharField(label=_('Departure city'))
    send_precise = forms.BooleanField(label=_('Send from address'), widget=forms.CheckboxInput(), required=False) # Отправить с адреса
    send_precise_address = forms.CharField(label=_('Departure address'), required=False,
                                           widget=forms.TextInput(attrs={'disabled': 'disabled'}))
    who_packs = forms.ChoiceField(label=_('Loading by'), choices=LOADING_BY)
    inner_transfer = forms.BooleanField(label=_('Inner transfer'), widget=forms.CheckboxInput(attrs={'class': 'checkbox'}), # Внутри области
                                        required=False)
    receiver_addr = forms.CharField(label=_('Delivery city'), required=False)
    receive_precise = forms.BooleanField(label=_('Deliver to address'), widget=forms.CheckboxInput(), required=False) # Доставить по адресу
    receive_precise_address = forms.CharField(label=_('Full delivery address'), required=False,
                                              widget=forms.TextInput(attrs={'disabled': 'disabled'}))
    who_unpacks = forms.ChoiceField(label=_('Unloading by'), choices=UNLOADING_BY)
    cargo_spaces = forms.IntegerField(label=_('Cargo spaces'), widget=forms.TextInput(attrs={'class': 'digits'}))
    cargo_weight = forms.FloatField(label=_('Cargo weight, kg'), widget=forms.TextInput(attrs={'class': 'digits'}))
    cargo_volume = forms.FloatField(label=_('Cargo volume, m3'), widget=forms.TextInput(attrs={'class': 'digits'}))
    cargo_value = forms.FloatField(label=_('Cargo value'), required=False,
                                   widget=forms.TextInput(attrs={'class': 'digits', 'disabled': 'disabled'}))
    package_type = forms.ChoiceField(label=_('Package type'), choices=PACKAGE_TYPES)
    insurance = forms.BooleanField(label=_('Insurance is required'), initial=False, required=False)
    extra_services = forms.ModelMultipleChoiceField(label=_('Extra services'), queryset=ExtraService.objects.all(),
                                                    widget=forms.CheckboxSelectMultiple(), required=False)
    
    def as_my_style(self):
        context = super().get_context()
        context['fields'] = {f_e[0].name: f_e[0] for f_e in context['fields']}
        context['hidden_fields'] = {f_e.name: f_e for f_e in context['hidden_fields']}
        return self.render(template_name='core/forms/calc_form.html', context=context)


class FeedbackForm(forms.Form):
    required_css_class = 'required'
    sub_name = forms.CharField(label=_('Your name'))
    sub_phone = forms.CharField(label=_('Your phone'), widget=forms.TextInput(attrs={'type': 'tel'}), required=False)
    sub_email = forms.EmailField(label=_('Your E-mail'), required=False)
    sub_title = forms.CharField(label=_('Topic'))
    sub_body = forms.CharField(label=_('Appeal'), widget=forms.Textarea())

    def as_my_style(self):
        context = super().get_context()
        context['fields'] = {f_e[0].name: f_e[0] for f_e in context['fields']}
        context['hidden_fields'] = {f_e.name: f_e for f_e in context['hidden_fields']}
        return self.render(template_name='core/forms/feedback_form.html', context=context)


class StatusForm(forms.Form):
    order_num = forms.CharField(label=None, widget=forms.TextInput(attrs={'placeholder': _('Enter order number')}))
