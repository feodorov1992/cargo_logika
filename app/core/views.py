import os

import gspread
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
from core.models import Document, IconBlock, PhotoBlock
from logistics.models import Order
from mailer.views import send_logo_mail


def get_from_spreadsheet(number):
    gc = gspread.service_account(os.path.join(settings.BASE_DIR, 'credentials/credentials.json'))
    sh = gc.open_by_key('1mFOIKA-DY5THkIXfvxfz8iKcHSfIdq0mU0HZu8LFSpU').sheet1
    status_dict = dict(sh.get_all_values()[1:])
    return status_dict.get(number)


def home(request):
    icon_blocks = IconBlock.objects.all()
    print(icon_blocks)
    return render(request, 'core/home.html', {'icon_blocks': icon_blocks})


class StatusFormView(FormView):
    form_class = StatusForm

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        order_num = form.cleaned_data.get('order_num')
        try:
            order = Order.objects.get(order_number=order_num)
            msg = render_to_string('core/messages/status_success.html', {'order': order})
        except ObjectDoesNotExist:
            old_status = get_from_spreadsheet(order_num)
            if old_status:
                msg = render_to_string('core/messages/status_old_school.html',
                                       {'order_number': order_num, 'status': old_status})
            else:
                msg = render_to_string('core/messages/status_error.html', {'order_num': order_num})

        messages.info(self.request, msg)
        return super(StatusFormView, self).form_valid(form)


class HomeView(StatusFormView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['icon_blocks'] = IconBlock.objects.all()
        context['photo_blocks'] = PhotoBlock.objects.all()
        return context


class ContactsView(StatusFormView):
    template_name = 'core/contacts.html'


class DocsView(StatusFormView):
    template_name = 'core/docs.html'


class ProjectsView(StatusFormView):
    template_name = 'core/projects.html'


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
