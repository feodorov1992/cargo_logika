from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

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
