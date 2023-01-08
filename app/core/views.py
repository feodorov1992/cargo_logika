from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import FormView
from django.utils.translation import gettext_lazy as _
from core.forms import CalcForm, FeedbackForm, StatusForm
from logistics.models import Order
from mailer.views import send_logo_mail


def home(request):
    return render(request, 'core/home.html', {})

class HomeView(FormView):
    form_class = StatusForm
    template_name = 'core/home.html'
    success_url = 'home'

    def get_success_url(self):
        return reverse(self.success_url)

    def form_valid(self, form):
        order_num = form.cleaned_data.get('order_num')
        try:
            order = Order.objects.get(order_number=order_num)
            msg = render_to_string('core/messages/status_success.html', {'order': order})
        except ObjectDoesNotExist:
            msg = render_to_string('core/messages/status_error.html', {'order_num': order_num})

        messages.info(self.request, msg)
        return super(HomeView, self).form_valid(form)


def contacts(request):
    return render(request, 'core/contacts.html', {})

def docs(request):
    return render(request, 'core/docs.html', {})

def projects(request):
    return render(request, 'core/projects.html', {})


class CalcView(FormView):
    form_class = CalcForm
    template_name = 'core/calc.html'
    success_url = 'calc'

    def get_success_url(self):
        return reverse(self.success_url)

    def form_valid(self, form):
        phone = form.cleaned_data.get('sub_phone')
        email = form.cleaned_data.get('sub_email')

        machine_fields = ('who_packs', 'who_unpacks', 'package_type')
        fields_to_join = ('cargo_warns', 'extra_services')

        context = {key: value for key, value in form.cleaned_data.items() if key not in machine_fields + fields_to_join}

        for field_name in machine_fields:
            mapper = {key: value for key, value in form.fields.get(field_name).choices}
            context[field_name] = mapper.get(form.cleaned_data.get(field_name))

        for field_name in fields_to_join:
            context[field_name] = ', '.join([str(i) for i in form.cleaned_data.get(field_name)])

        send_logo_mail(
            _('Order price calculation request from site'),
            render_to_string('core/mail/calc.txt', context),
            render_to_string('core/mail/calc.html', context),
            'calc@cargo-logika.ru',
            [settings.EMAIL_ADMIN_ADDRESS]
        )

        msg = render_to_string('core/messages/calc_success.html', {'phone': phone, 'email': email})
        messages.success(self.request, msg)

        return super(CalcView, self).form_valid(form)


class FeedbackView(FormView):
    form_class = FeedbackForm
    template_name = 'core/feedback.html'
    success_url = 'feedback'

    def get_success_url(self):
        return reverse(self.success_url)

    def form_valid(self, form):
        name = form.cleaned_data.get('sub_name')
        phone = form.cleaned_data.get('sub_phone')
        email = form.cleaned_data.get('sub_email')

        send_logo_mail(
            _('New feedback from site'),
            render_to_string('core/mail/feedback.txt', form.cleaned_data),
            render_to_string('core/mail/feedback.html', form.cleaned_data),
            'feedback@cargo-logika.ru',
            [settings.EMAIL_ADMIN_ADDRESS]
        )

        msg = render_to_string('core/messages/feedback_success.html', {'name': name, 'phone': phone, 'email': email})
        messages.success(self.request, msg)

        return super(FeedbackView, self).form_valid(form)