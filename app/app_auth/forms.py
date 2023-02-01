from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from app_auth.models import User
from dadata import Dadata

from logistics.models import Order


class UserCreateForm(UserCreationForm):
    required_css_class = 'required'

    email = forms.EmailField(required=True, label=_('Your E-mail'))
    tin = forms.CharField(required=True, label=_('User TIN'))

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.org_name_suggenstions = list()

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

    def get_org_name_by_tin(self, tin):
        dadata = Dadata(settings.DADATA_TOKEN)
        self.org_name_suggenstions = [i['value'] for i in dadata.find_by_id('party', tin)]
        return self.org_name_suggenstions

    def clean_tin(self):
        data = self.cleaned_data['tin']
        if data and User.objects.filter(tin=data).exists():
            raise ValidationError(_('User with such TIN already exists'))
        if data and not self.get_org_name_by_tin(data):
            raise ValidationError(_('Company with such TIN does not exist'))
        return data

    def save(self, commit=True):
        result = super(UserCreateForm, self).save(False)
        result.username = result.email
        result.org_name = self.org_name_suggenstions[0]
        if commit:
            result.save()
            Order.objects.filter(payer_tin=result.tin).update(payer_name=result.org_name, user=result)
        return result

    class Meta:
        model = User
        fields = ['email', 'tin']