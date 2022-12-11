from django.urls import path

from dynamic_docs.views import receipt

urlpatterns = [
    path('<uuid:order_pk>/receipt/<str:filename>', receipt, name='receipt')
]
