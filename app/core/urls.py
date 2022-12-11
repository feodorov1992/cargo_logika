from django.urls import path, include

from core.views import home, contacts, docs, projects, CalcView, FeedbackView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts', contacts, name='contacts'),
    path('docs', docs, name='docs'),
    path('projects', projects, name='projects'),
    path('calc', CalcView.as_view(), name='calc'),
    path('feedback', FeedbackView.as_view(), name='feedback'),
    path('order/', include('logistics.urls'))
]
