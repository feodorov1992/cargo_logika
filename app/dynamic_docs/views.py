from django.shortcuts import render

from dynamic_docs.generator import PDFGenerator
from logistics.models import Order, DeliveryType, ExtraService


def receipt(request, order_pk, filename):
    order = Order.objects.get(pk=order_pk)
    generator = PDFGenerator(filename)
    return generator.response('dynamic_docs/receipt.html', {
        'filename': filename, 'order': order,
        'delivery_types': DeliveryType.objects.all(),
        'extra_services': ExtraService.objects.all()
    })
