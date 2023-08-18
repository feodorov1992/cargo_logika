from django.urls import path, include

from core.views import CalcView, FeedbackView, HomeView, ContactsView, DocsView, ProjectsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('docs/', DocsView.as_view(), name='docs'),
    path('projects/', ProjectsView.as_view(), name='projects'),
    path('calc/', CalcView.as_view(), name='calc'),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
]
