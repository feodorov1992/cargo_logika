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
    exclude = ('extra_info', 'pickup_date_wanted', 'delivery_date_wanted', 'cargo_name', 'package_type', 'cargo_spaces',
               'cargo_weight', 'cargo_volume', 'insurance', 'cargo_value', )

    def get_success_message(self, cleaned_data):
        return render_to_string('logistics/messages/order_success.html',
                                {'order_number': self.object.order_number, 'mail_to': self.object.payer_email})

    def get_success_url(self):
        return reverse('order')

    def get_form(self, form_class=None):
        form = super(OrderCreateView, self).get_form(form_class)
        order_pk = self.request.GET.get('repeat')
        if order_pk:
            repeat_order = Order.objects.get(pk=order_pk)
            form.initial = repeat_order.__dict__
            for field in self.exclude:
                form.initial.pop(field)
            form.initial['extra_services'] = [i.pk for i in repeat_order.extra_services.all()]
        return form

    def form_valid(self, form):
        response = super(OrderCreateView, self).form_valid(form)
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            self.object.user = self.request.user
            self.object.save()
        return response
