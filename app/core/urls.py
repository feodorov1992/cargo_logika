from django.urls import path

from core.views import home, contacts, docs

urlpatterns = [
    path('', home, name='home'),
    path('contacts', contacts, name='contacts'),
    path('docs', docs, name='docs')
]
