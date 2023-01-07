import time
import uuid

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from app.celery import app
from app_auth.models import User, CP_TYPES
from log_cats.models import ExtraService, DeliveryType
from mailer.views import send_logo_mail


PAYMENT_TYPES = (
    ('cash', _('Cash payment')),
    ('cashless', _('Cashless payment'))
)


PACKAGE_TYPES = (
    ('pallet', _('Pallet')),
    ('bulk', _('Bulk'))
)

LOADING_BY = (
    ('cargo_logika', _('Loading by "CARGO LOGIKA"')),
    ('sender', _('Loading by sender'))
)

UNLOADING_BY = (
    ('cargo_logika', _('Unloading by "CARGO LOGIKA"')),
    ('receiver', _('Unloading by receiver'))
)

DOCS_SENT_CHOICES = (
    ('no', _('No')),
    ('yes', _('Yes')),
    ('edm', _('EDM'))
)


def default_order_num():
    if Order.objects.exists():
        try:
            return int(Order.objects.first().order_number) + 1
        except ValueError:
            return settings.INITIAL_ORDER_NUMBER + Order.objects.count()
    else:
        return settings.INITIAL_ORDER_NUMBER

@app.task(bind=True)
def send_model_email(self, subject, template_name, model_path, obj_pk, from_email, recipients):
    app_label, _, class_name = model_path.split('.')
    model = apps.get_model(app_label, class_name)
    obj = model.objects.get(pk=obj_pk)
    body_text = render_to_string(f'{template_name}.txt', {'object': obj})
    body_html = render_to_string(f'{template_name}.html', {'object': obj})
    return send_logo_mail(subject, body_text, body_html, from_email, recipients)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4) #
    created_at = models.DateTimeField(auto_now_add=True, editable=False) #
    updated_at = models.DateTimeField(auto_now=True, editable=False) #
    order_number = models.CharField(default=default_order_num, verbose_name=_('Order number'), max_length=7) #
    order_date = models.DateField(default=timezone.now, verbose_name=_('Order date')) #
    payer_name = models.CharField(max_length=255, verbose_name=_('Payer')) #
    payment_type = models.CharField(max_length=15, verbose_name=_('Payment type'), choices=PAYMENT_TYPES, #
                                    default=PAYMENT_TYPES[0][0]) #
    payer_tin = models.CharField(max_length=15, verbose_name=_('Payer TIN')) #
    payer_email = models.EmailField(verbose_name=_('Payer email')) #
    payer_phone = models.CharField(max_length=50, verbose_name=_('Payer phone')) #
    payer_contact = models.CharField(max_length=100, verbose_name=_('Payer contact')) #
    cargo_name = models.CharField(max_length=255, verbose_name=_('Cargo name')) #
    package_type = models.CharField(max_length=15, verbose_name=_('Package type'), choices=PACKAGE_TYPES, #
                                    default=PACKAGE_TYPES[0][0]) #
    extra_services = models.ManyToManyField(ExtraService, verbose_name=_('Extra services'), blank=True) #
    cargo_spaces = models.IntegerField(verbose_name=_('Cargo spaces')) #
    cargo_weight = models.FloatField(verbose_name=_('Cargo weight, kg')) #
    cargo_volume = models.FloatField(verbose_name=_('Cargo volume, m3')) #
    insurance = models.BooleanField(verbose_name=_('Insurance is required'), default=False) #
    cargo_value = models.FloatField(verbose_name=_('Cargo value')) #
    sender_name = models.CharField(max_length=255, verbose_name=_('Sender')) #
    sender_type = models.CharField(max_length=15, verbose_name=_('Sender type'), choices=CP_TYPES, #
                                   default=CP_TYPES[0][0]) #
    sender_passport = models.CharField(max_length=30, verbose_name=_('Sender passport'), blank=True, null=True) #
    sender_tin = models.CharField(max_length=15, verbose_name=_('Sender TIN'), blank=True, null=True) #
    sender_phone = models.CharField(max_length=50, verbose_name=_('Sender phone')) #
    sender_contact = models.CharField(max_length=100, verbose_name=_('Sender contact')) #
    sender_addr = models.CharField(max_length=255, verbose_name=_('Departure city')) #
    send_precise_address = models.CharField(max_length=255, verbose_name=_('Departure address'), blank=True, null=True) #
    loading_by = models.CharField(max_length=30, verbose_name=_('Loading by'), choices=LOADING_BY, #
                                  default=LOADING_BY[0][0]) #
    receiver_name = models.CharField(max_length=255, verbose_name=_('Receiver')) #
    receiver_type = models.CharField(max_length=15, verbose_name=_('Receiver type'), choices=CP_TYPES, #
                                     default=CP_TYPES[0][0]) #
    receiver_passport = models.CharField(max_length=30, verbose_name=_('Receiver passport'), blank=True, null=True) #
    receiver_tin = models.CharField(max_length=15, verbose_name=_('Receiver TIN'), blank=True, null=True) #
    receiver_phone = models.CharField(max_length=50, verbose_name=_('Receiver phone')) #
    receiver_contact = models.CharField(max_length=100, verbose_name=_('Receiver contact')) #
    receiver_addr = models.CharField(max_length=255, verbose_name=_('Delivery city')) #
    receiver_precise_address = models.CharField(max_length=255, verbose_name=_('Full delivery address'), #
                                                blank=True, null=True) #
    unloading_by = models.CharField(max_length=30, verbose_name=_('Unloading by'), choices=UNLOADING_BY, #
                                    default=UNLOADING_BY[0][0]) #
    delivery_type = models.ForeignKey(DeliveryType, verbose_name=_('Type of delivery'),
                                      default=DeliveryType.get_default_pk, on_delete=models.PROTECT) #
    extra_info = models.TextField(verbose_name=_('Extra info'), blank=True, null=True) #
    pickup_date_wanted = models.DateField(verbose_name=_('Wanted date of pickup'))
    pickup_date = models.DateField(verbose_name=_('Date of pickup'), blank=True, null=True) #
    picked_up = models.BooleanField(verbose_name=_('Cargo picked up'), default=False) #
    delivery_date_wanted = models.DateField(verbose_name=_('Wanted date of delivery'), blank=True, null=True)
    delivery_date = models.DateField(verbose_name=_('Date of delivery'), blank=True, null=True) #
    delivered = models.BooleanField(verbose_name=_('Cargo delivered'), default=False) #
    docs_sent = models.CharField(max_length=5, verbose_name=_('Docs sent'), choices=DOCS_SENT_CHOICES, #
                                    default=DOCS_SENT_CHOICES[0][0]) #
    contractor = models.CharField(max_length=255, verbose_name=_('Contractor'), blank=True, null=True) #
    contractor_waybill = models.CharField(max_length=50, verbose_name=_('Contractor waybill'), blank=True, null=True) #
    expenses = models.FloatField(verbose_name=_('Transit expenses, rub'), blank=True, null=True) #
    order_price = models.FloatField(verbose_name=_('Transit price, rub'), blank=True, null=True) #
    insurance_price = models.FloatField(verbose_name=_('Insurance price, rub'), blank=True, null=True) #
    insurance_number = models.CharField(max_length=50, verbose_name=_('Insurance bill number'), blank=True, null=True) #
    bill_date = models.DateField(verbose_name=_('Date of bill'), blank=True, null=True) #
    bill_sent = models.BooleanField(verbose_name=_('Bill sent'), default=False) #
    bill_payed = models.BooleanField(verbose_name=_('Bill payed'), default=False) #
    load_unload = models.BooleanField(verbose_name=_('Loading/unloading required'), default=True) #
    hidden_status = models.CharField(max_length=255, verbose_name=_('Hidden status'), blank=True, null=True)
    contract = models.CharField(max_length=255, verbose_name=_('Contract number'), blank=True, null=True) #
    accounts_email_sent = models.BooleanField(verbose_name=_('Email to the accounts manager sent'), default=False) #
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Submitted by'),
                             related_name='orders')

    def status(self):
        last_status = None
        if self.statuses.exists():
            last_status = self.statuses.last()
        result = [i for i in (last_status.label, self.hidden_status) if i]
        return ', '.join(result) if result else None

    status.short_description = _('Status')

    def from_addr(self):
        result = [i for i in (self.sender_addr, self.send_precise_address) if i]
        return ', '.join(result) if result else None

    from_addr.short_description = _('Pickup address')

    def to_addr(self):
        result = [i for i in (self.receiver_addr, self.receiver_precise_address) if i]
        return ', '.join(result) if result else None

    to_addr.short_description = _('Delivery address')

    def __str__(self):
        return _('Order #{} dated {}').format(self.order_number, self.order_date.strftime('%d.%m.%Y'))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.loading_by == 'cargo_logika' or self.unloading_by == 'cargo_logika':
            self.load_unload = True
        else:
            self.load_unload = False
        if self.user:
            if not self.contract:
                self.contract = self.user.contract
        if not self.picked_up:
            if self.pickup_date and self.pickup_date <= timezone.now().date():
                self.picked_up = True
        if not self.delivered:
            if self.delivery_date and self.delivery_date <= timezone.now().date():
                self.delivered = True
        super(Order, self).save(force_insert, force_update, using, update_fields)

    def receipt_filename(self):
        return f'ЭР_{self.order_number}.pdf'

    def clean(self):
        errors = dict()
        if self.payer_type == 'individual' and not self.payer_passport:
            errors['payer_passport'] = _('Passport number is required for paying individuals')
        if self.payer_type == 'company' and not self.payer_tin:
            errors['payer_tin'] = _('TIN is required for paying companies')
        if self.sender_type == 'individual' and not self.sender_passport:
            errors['sender_passport'] = _('Passport number is required for sending individuals')
        if self.sender_type == 'company' and not self.sender_tin:
            errors['sender_tin'] = _('TIN is required for sending companies')
        if self.receiver_type == 'individual' and not self.receiver_passport:
            errors['receiver_passport'] = _('Passport number is required for receiving individuals')
        if self.receiver_type == 'company' and not self.receiver_tin:
            errors['receiver_tin'] = _('TIN is required for receiving companies')
        if self.insurance and not self.cargo_value:
            errors['cargo_value'] = _('Cargo value is required for insurance')
        if errors:
            raise ValidationError(errors)

    def send_creation_email(self, mail_type='admin'):
        subject = _('New order No.') + str(self.order_number)
        from_email = 'order@cargo-logika.ru'
        if mail_type == 'admin':
            template_name = 'logistics/mail/order_admin'
            recipients = [settings.EMAIL_ADMIN_ADDRESS, settings.EMAIL_LOGIST_ADDRESS]
        elif mail_type == 'user':
            template_name = 'logistics/mail/order_user'
            recipients = [self.payer_email]
        else:
            return
        return send_model_email.delay(subject, template_name, 'logistics.models.Order', self.pk, from_email, recipients)


    class Meta:
        ordering = ['-order_number']
        verbose_name = _('order')
        verbose_name_plural = _('orders')


class OrderStatus(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    order = models.ForeignKey(Order, verbose_name=_('Order'), on_delete=models.CASCADE, related_name='statuses')
    label = models.CharField(max_length=255, verbose_name=_('Status label'))
    date = models.DateField(default=timezone.now, verbose_name=_('Date of status change'))

    def __str__(self):
        return _('{}: {} (order #{})').format(self.date.strftime('%d.%m.%Y'), self.label, self.order.order_number)

    # def send_creation_email(self):
    #     subject = _('Order No.{} status update')
    #     template_name = 'logistics/mail/status_user'
    #     from_email = 'order@cargo-logika.ru'
    #     recipients = [self.order.payer_email]
    #     return send_model_email(subject, template_name, self, from_email, recipients)

    class Meta:
        verbose_name = _('order status')
        verbose_name_plural = _('order statuses')
        ordering = ['created_at']


@receiver(post_save, sender=Order)
def save_order(sender, instance, created, **kwargs):
    if created:
        OrderStatus.objects.create(label=_('New'), order=instance)
        instance.send_creation_email()
        instance.send_creation_email('user')


@receiver(post_save, sender=User)
def save_user(sender, instance, created, **kwargs):
    if not instance.is_staff:
        Order.objects.filter(Q(payer_tin=instance.tin) |
                             Q(sender_tin=instance.tin) |
                             Q(receiver_tin=instance.tin),
                             user__isnull=True).update(user=instance)

# @receiver(post_save, sender=OrderStatus)
# def save_status(sender, instance, created, **kwargs):
#     if created and instance.label != _('New'):
#         instance.send_creation_email()
