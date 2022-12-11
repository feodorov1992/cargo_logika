from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import CreateView

from logistics.forms import OrderForm
from logistics.models import Order


class OrderCreateView(SuccessMessageMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'logistics/order.html'

    def get_success_message(self, cleaned_data):
        return render_to_string('logistics/messages/order_success.html',
                                {'order_number': self.object.order_number, 'mail_to': self.object.payer_email})

    def get_success_url(self):
        return reverse('order')