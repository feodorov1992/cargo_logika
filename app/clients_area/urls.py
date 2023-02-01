from django.urls import path

from clients_area.views import OrderListView

urlpatterns = [
    path('', OrderListView.as_view(), name='orders_list')
]
