from django.urls import path

from clients_area.views import OrderListView, OrderDetailView

urlpatterns = [
    path('', OrderListView.as_view(), name='orders_list'),
    path('<uuid:pk>', OrderDetailView.as_view(), name='order_detail')
]
