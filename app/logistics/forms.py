from django import forms

from logistics.models import Order


class OrderForm(forms.ModelForm):
    required_css_class = 'required'

    def as_my_style(self):
        context = super().get_context()
        context['fields'] = {f_e[0].name: f_e[0] for f_e in context['fields']}
        context['hidden_fields'] = {f_e.name: f_e for f_e in context['hidden_fields']}
        return self.render(template_name='logistics/forms/order_form.html', context=context)

    class Meta:
        model = Order
        exclude = ['order_number', 'order_date', 'pickup_date', 'docs_sent', 'contractor_waybill', 'expenses',
                   'order_price', 'insurance_price', 'insurance_number', 'bill_sent', 'bill_payed']
        widgets = {
            'extra_cargo_params': forms.CheckboxSelectMultiple(),
            'extra_services': forms.CheckboxSelectMultiple(),
            'delivery_type': forms.CheckboxSelectMultiple(),
            'package_type': forms.RadioSelect(),
            'insurance': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'cargo_spaces': forms.NumberInput(attrs={'class': 'digits'}),
            'cargo_weight': forms.NumberInput(attrs={'class': 'digits'}),
            'cargo_volume': forms.NumberInput(attrs={'class': 'digits'}),
            'cargo_value': forms.NumberInput(attrs={'class': 'digits'}),
            'send_precise_address': forms.TextInput(attrs={'disabled': 'disabled'}),
            'receiver_precise_address': forms.TextInput(attrs={'disabled': 'disabled'}),
        }
