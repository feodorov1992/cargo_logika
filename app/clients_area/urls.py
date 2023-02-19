from django.urls import path

from clients_area.views import OrderListView, OrderDetailView, XLSReportView

urlpatterns = [
    path('', OrderListView.as_view(), name='orders_list'),
    path('<uuid:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('report', XLSReportView.as_view(), name='XLS_client')
]
