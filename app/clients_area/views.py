from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _

from dynamic_docs.generator import XLSGenerator
from logistics.models import Order


class OrderListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Order
    template_name = 'clients_area/orders_list.html'

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset


class OrderDetailView(UserPassesTestMixin, DetailView):
    model = Order
    template_name = 'clients_area/order_detail.html'

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.user or self.request.user.is_staff


class XLSReportView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Order

    def get_queryset(self):
        queryset = super(XLSReportView, self).get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        fields = ['order_number', 'order_date', 'status_pub', 'payer_name', 'payment_type', 'payer_tin', 'payer_email',
                  'payer_phone', 'payer_contact', 'cargo_name', 'package_type', 'extra_services', 'cargo_spaces',
                  'cargo_weight', 'cargo_volume', 'cargo_value', 'insurance', 'delivery_type', 'insurance_number',
                  'insurance_price', 'order_price', 'sender_name', 'sender_type', 'sender_passport', 'sender_tin',
                  'sender_phone', 'sender_contact', 'sender_addr', 'send_precise_address', 'pickup_date_wanted',
                  'pickup_date', 'loading_by', 'receiver_name', 'receiver_type', 'receiver_passport', 'receiver_tin',
                  'receiver_phone', 'receiver_contact', 'receiver_addr', 'receiver_precise_address',
                  'delivery_date_wanted', 'delivery_date', 'unloading_by', 'extra_info']
        mapper = {'status_pub': _('Status'), 'status_date': _('Date of status change')}

        if request.user.is_staff:
            filename = 'report.xls'
        else:
            filename = f'{request.user.org_name} {timezone.now().strftime("%d.%m.%Y")}.xls'
        gen = XLSGenerator(Order, fields, mapper)
        return gen.response(queryset, filename)
