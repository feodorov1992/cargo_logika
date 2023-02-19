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
        fields = ['order_number', 'order_date', 'status_pub', 'status_date', 'docs_sent', 'payer_name', 'sender_name',
                  'from_addr', 'cargo_spaces', 'cargo_weight', 'cargo_volume', 'receiver_name', 'to_addr',
                  'load_unload', 'extra_services', 'order_price', 'cargo_value', 'insurance_price', 'insurance_number']
        mapper = {'status_pub': _('Status'), 'status_date': _('Date of status change'),
                  'from_addr': _('Pickup address'), 'to_addr': _('Delivery address')}

        if request.user.is_staff:
            filename = 'report.xls'
        else:
            filename = f'{request.user.org_name} {timezone.now().strftime("%d.%m.%Y")}.xls'
        gen = XLSGenerator(Order, fields, mapper)
        return gen.response(queryset, filename)
