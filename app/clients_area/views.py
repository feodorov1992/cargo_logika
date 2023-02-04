from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView

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
