from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path

from app_auth.views import UserAuthView, UserCreateView, UserUpdateView, UserPasswordChangeView, UserPasswordResetView, \
    UserPasswordResetDoneView, UserPasswordResetConfirmView, UserPasswordResetCompleteView

urlpatterns = [
    path('login/', UserAuthView.as_view(), name='login'),
    path('sign_up/', UserCreateView.as_view(), name='sign_up'),
    path('edit_profile/', UserUpdateView.as_view(), name='edit_profile'),
    path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),

    path('reset_password/', UserPasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
