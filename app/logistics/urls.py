from django.urls import path

from logistics.views import OrderCreateView

urlpatterns = [
    path('', OrderCreateView.as_view(), name='order')
]
