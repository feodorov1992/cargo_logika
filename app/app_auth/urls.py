from django.urls import path

from app_auth.views import UserAuthView, UserCreateView

urlpatterns = [
    path('login/', UserAuthView.as_view(), name='login'),
    path('sign_up/', UserCreateView.as_view(), name='sign_up'),
]
