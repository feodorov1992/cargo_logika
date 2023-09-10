import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _

from clients_area.forms import ClientsAreaOrdersFilters
from dynamic_docs.generator import XLSGenerator
from logistics.models import Order


class OrderFilteringMixin:

    def get_queryset(self, **additional_filters):
        if self.request.user.is_staff:
            return Order.objects.filter(**additional_filters)
        return Order.objects.filter(user=self.request.user, **additional_filters)

    @staticmethod
    def collect_date_params(get_params: QueryDict, allowed_keys: list = None):
        result = dict()
        for key, value in get_params.items():
            try:
                if value is not None and (allowed_keys is None or key in allowed_keys):
                    result[key] = datetime.date.fromisoformat(value)
            except TypeError:
                continue
            except ValueError:
                continue
        return result


class OrderListView(LoginRequiredMixin, OrderFilteringMixin, View):
    login_url = 'login'
    model = Order
    template_name = 'clients_area/orders_list.html'

    def get_queryset(self, **additional_filters):
        if self.request.user.is_staff:
            return Order.objects.filter(**additional_filters)
        return Order.objects.filter(user=self.request.user, **additional_filters)

    def get(self, request):
        form = ClientsAreaOrdersFilters()
        if request.GET:
            actual_params = self.collect_date_params(request.GET, form.fields.keys())
            form.initial = actual_params
            queryset = self.get_queryset(**actual_params)
        else:
            queryset = self.get_queryset()
        return render(request, 'clients_area/orders_list.html', {'form': form, 'object_list': queryset})

    def post(self, request):
        form = ClientsAreaOrdersFilters(request.POST)
        queryset = self.get_queryset()
        if form.is_valid():
            redirect_url = reverse('orders_list')
            get_params = QueryDict('', mutable=True)
            get_params.update({k: v for k, v in form.cleaned_data.items() if v is not None})
            if get_params:
                redirect_url = '?'.join([redirect_url, get_params.urlencode().lower()])
            return redirect(redirect_url)
        return render(request, 'clients_area/orders_list.html', {'form': form, 'object_list': queryset})


class OrderDetailView(UserPassesTestMixin, DetailView):
    model = Order
    template_name = 'clients_area/order_detail.html'

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.user or self.request.user.is_staff


class XLSReportView(LoginRequiredMixin, OrderFilteringMixin, ListView):
    login_url = 'login'
    model = Order

    def get(self, request, *args, **kwargs):
        if request.GET:
            queryset = self.get_queryset(**self.collect_date_params(request.GET))
        else:
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
