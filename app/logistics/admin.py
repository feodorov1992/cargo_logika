from datetime import datetime

from django import forms
from django.conf import settings
from django.contrib import admin, messages
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from logistics.models import Order, OrderStatus
from mailer.views import send_logo_mail


class OrderStatusInline(admin.TabularInline):
    model = OrderStatus
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('order_number', 'order_date',),
                       ('payer_name', 'payer_tin', 'user'))
        }),
        (_('Payer info'), {
            'fields': (('payment_type', 'contract'),
                       ('payer_email', 'payer_phone', 'payer_contact')),
            'classes': ('collapse',),
        }),
        (_('Send/receive info'), {
            'fields': (('sender_name', 'receiver_name'),
                       ('sender_tin', 'receiver_tin'),
                       ('sender_passport', 'receiver_passport'),
                       ('sender_addr', 'receiver_addr'),
                       ('send_precise_address', 'receiver_precise_address'),
                       ('loading_by', 'unloading_by'),
                       ('sender_type', 'receiver_type'),
                       ('sender_contact', 'receiver_contact'),
                       ('sender_phone', 'receiver_phone'),
                       ('hidden_status',),
                       ('delivery_type', 'extra_services', 'load_unload', 'insurance'),
                       'extra_info'
                       )
        }),
        (_('Pickup/delivery info'), {
            'fields': (('pickup_date_wanted', 'delivery_date_wanted'),
                       ('pickup_date', 'delivery_date'),
                       ('picked_up', 'delivered'))
        }),
        (_('Cargo info'), {
            'fields': (('cargo_name', 'package_type', 'cargo_value'),
                       ('cargo_spaces', 'cargo_weight', 'cargo_volume'))
        }),
        (_('Financial info'), {
            'fields': (('order_price', 'expenses'),
                       ('contractor', 'contractor_waybill'),
                       ('insurance_price', 'insurance_number'),
                       ('bill_date', 'bill_sent', 'bill_payed', 'docs_sent'),
                       'accounts_email_sent'),
            'classes': ('collapse',),
        }),
    )

    inlines = (OrderStatusInline, )

    actions = ['send_accounts_email_action', 'send_registry_email_action']
    change_form_template = 'admin/order_edit.html'
    list_filter = (
        'payer_name', 'picked_up', 'delivered', 'insurance', 'docs_sent', 'delivery_type',
        'accounts_email_sent', 'bill_sent', 'bill_payed', 'load_unload', 'extra_services',
    )

    search_fields = ('order_number', )

    list_display = ('order_number', 'order_date', 'pickup_date', 'status', 'docs_sent', 'payer_name', 'sender_name',
                    'from_addr', 'cargo_spaces', 'cargo_weight', 'cargo_volume', 'receiver_name', 'to_addr',
                    'load_unload', 'contractor', 'contractor_waybill', 'expenses', 'order_price', 'cargo_value',
                    'insurance_price', 'insurance_number')

    formfield_overrides = {
        models.ManyToManyField: {'widget': forms.CheckboxSelectMultiple}
    }

    @staticmethod
    def get_payer_type_label(queryset):
        if all([i.payer_type == 'individual' for i in queryset]):
            return _('Passport')
        elif all([i.payer_type == 'company' for i in queryset]):
            return _('Payer TIN')
        return f"{_('Payer TIN')}/{_('Passport')}"

    def send_accounts_email(self, queryset, user):
        context = {'user': user, 'queryset': queryset, 'payer_id_label': self.get_payer_type_label(queryset)}

        mail_status = send_logo_mail(
            _('Bills issue request'),
            render_to_string('logistics/mail/accounts_email.txt', context),
            render_to_string('logistics/mail/accounts_email.html', context),
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_ACCOUNTS_ADDRESS]
        )

        if mail_status == 1:
            queryset.update(accounts_email_sent=True)

    @staticmethod
    def collect_missing_order_fields(obj, mapper: dict, one_of: dict, conditional: dict):
        if one_of is None:
            one_of = {}
        one_of.update({v: k for k, v in one_of.items()})
        missing_verbose = list()
        for field_name, field_verbose in mapper.items():
            if field_name in one_of:
                field_rev_name =  one_of[field_name]
                field_rev_verbose = mapper[field_rev_name]
                if not (obj.__getattribute__(field_name) or obj.__getattribute__(field_rev_name)):
                    msg = _('{} or {}').format(field_verbose, field_rev_verbose)
                    rev_msg = _('{} or {}').format(field_rev_verbose, field_verbose)
                    if not (msg in missing_verbose or rev_msg in missing_verbose):
                        missing_verbose.append(msg)
            elif field_name in conditional:
                cond_field_name = conditional[field_name]
                if obj.__getattribute__(cond_field_name) and not obj.__getattribute__(field_name):
                    missing_verbose.append(field_verbose)
            else:
                if not obj.__getattribute__(field_name):
                    missing_verbose.append(field_verbose)


        return ', '.join(missing_verbose)

    def collect_errors(self, queryset, mapper: dict, one_of: dict = None, conditional: dict = None):
        errors = list()
        for order in queryset:
            missing = self.collect_missing_order_fields(order, mapper, one_of, conditional)
            if missing:
                errors.append((order.order_number, missing))
        return errors

    def send_accounts_email_action(self, request, queryset):
        mapper = {
            'bill_date': 'дата выставления счета',
            'delivery_date': 'дата доставки',
            'order_price': 'стоимость перевозки',
            'insurance_price': 'стоимость страховки',
            'insurance_number': '№ полиса'
        }
        one_of = {'bill_date': 'delivery_date'}
        conditional = {
            'insurance_price': 'insurance',
            'insurance_number': 'insurance'
        }
        errors = self.collect_errors(queryset, mapper, one_of, conditional)
        if errors:
            error_list = [f'{o_num}: {o_ver}' for o_num, o_ver in errors]
            self.message_user(
                request,
                format_html(_('Essential info is missing in orders:<br>{}').format('<br>'.join(error_list))),
                messages.ERROR
            )
        else:
            self.send_accounts_email(queryset, request.user)
            self.message_user(
                request,
                _('Accounts manager ordered to issue bills')
            )

    @staticmethod
    def get_sum_price(queryset):
        result = float()
        for order in queryset:
            result += order.order_price
            if order.insurance:
                result += order.insurance_price
        return result

    def send_registry_email(self, request, queryset, bill_number, bill_date, payer, payer_id):
        context = {
            'user': request.user,
            'queryset': queryset,
            'payer_id_label': self.get_payer_type_label(queryset),
            'bill_number': bill_number,
            'bill_date': bill_date,
            'payer': payer,
            'payer_id': payer_id,
            'sum_price': self.get_sum_price(queryset)
        }
        mail_status = send_logo_mail(
            _('Registry bill issue request'),
            render_to_string('logistics/mail/accounts_registry_email.txt', context),
            render_to_string('logistics/mail/accounts_registry_email.html', context),
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_ACCOUNTS_ADDRESS]
        )

        if mail_status == 1:
            queryset.update(accounts_email_sent=True)

    def send_registry_email_action(self, request, queryset):
        mapper = {
            'order_price': 'стоимость перевозки',
            'insurance_price': 'стоимость страховки',
            'insurance_number': '№ полиса'
        }
        conditional = {
            'insurance_price': 'insurance',
            'insurance_number': 'insurance'
        }
        errors = self.collect_errors(queryset, mapper, {}, conditional)
        if errors:
            error_list = [f'{o_num}: {o_ver}' for o_num, o_ver in errors]
            self.message_user(
                request,
                format_html(_('Essential info is missing in orders:<br>{}').format('<br>'.join(error_list))),
                messages.ERROR
            )
        else:
            if 'apply' in request.POST:

                self.send_registry_email(
                    request, queryset,
                    request.POST.get('bill_number'),
                    datetime.fromisoformat(request.POST.get('bill_date')).date(),
                    request.POST.get('payer'),
                    request.POST.get('payer_id')
                )
                queryset.update(accounts_email_sent=True)
                self.message_user(
                    request,
                    _('Accounts manager ordered to issue registry bill')
                )
                return HttpResponseRedirect(request.get_full_path())
            return render(request, 'admin/registry_data.html', {'orders': queryset})

    send_accounts_email_action.short_description = _('Send bills request to the accounts manager')
    send_registry_email_action.short_description = _('Send registry bill request to the accounts manager')
