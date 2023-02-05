from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from app_auth.models import User
from dadata import Dadata
from django.template import loader
from logistics.models import Order
from mailer.views import send_logo_mail


class UserCreateForm(UserCreationForm):
    required_css_class = 'required'

    email = forms.EmailField(label=_('Login (E-mail)'), max_length=254, required=True,
                             widget=forms.EmailInput(attrs={'autocomplete': 'email'}))
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
            context = {
                'user': result
            }
            send_logo_mail(
                subject=_('Thank you for registration on cargo-logika.ru!'),
                body_text=loader.render_to_string('app_auth/mail/greetings.txt', context),
                body_html=loader.render_to_string('app_auth/mail/greetings.html', context),
                from_email='register@cargo-logika.ru',
                recipients=[result.email]
            )
        return result

    class Meta:
        model = User
        fields = ['email', 'tin']


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(label=_('Login (E-mail)'), max_length=254,
                             widget=forms.EmailInput(attrs={'autocomplete': 'email'}))

    def save(self, commit=True):
        result = super(UserEditForm, self).save(False)
        result.username = result.email
        return result

    class Meta:
        model = User
        fields = ['email']


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_('Login (E-mail)'), max_length=254,
                             widget=forms.EmailInput(attrs={'autocomplete': 'email'}))

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        subject = loader.render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        return send_logo_mail(
            subject=subject,
            body_text=loader.render_to_string(email_template_name, context),
            body_html=loader.render_to_string(html_email_template_name, context),
            from_email=from_email,
            recipients=[to_email]
        )


class UserLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.EmailInput(attrs={'autofocus': True, 'autocomplete': 'email'}),
                             label=_('Login (E-mail)'))
