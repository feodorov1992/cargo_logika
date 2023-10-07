from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import UpdateView

from app_auth.forms import UserCreateForm, UserEditForm, UserPasswordResetForm, UserLoginForm, UserPasswordChangeForm


class UserAuthView(LoginView):
    template_name = 'app_auth/login.html'
    form_class = UserLoginForm

    def get_success_url(self):
        return reverse('orders_list')


class UserCreateView(View):
    def get(self, request):
        form = UserCreateForm()
        return render(request, 'app_auth/sign_up.html', {'form': form})

    def post(self, request):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('orders_list')
        return render(request, 'app_auth/sign_up.html', {'form': form})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    template_name = 'app_auth/edit_profile.html'
    form_class = UserEditForm

    def get_success_url(self):
        return reverse('orders_list')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'app_auth/password_change.html'
    login_url = 'login'
    form_class = UserPasswordChangeForm

    def get_form(self, form_class=None):
        form = super(UserPasswordChangeView, self).get_form(form_class)
        form.required_css_class = 'required'
        form.fields['new_password1'].help_text = None
        form.fields['new_password2'].help_text = None
        return form

    def get_success_url(self):
        return reverse('orders_list')


class UserPasswordResetView(PasswordResetView):
    from_email = 'register@cargo-logika.ru'
    template_name = 'app_auth/password_reset.html'
    email_template_name = 'app_auth/mail/reset_password_email.txt'
    html_email_template_name = 'app_auth/mail/reset_password_email.html'
    form_class = UserPasswordResetForm


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'app_auth/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'app_auth/password_reset_confirm.html'

    def get_success_url(self):
        url = super(UserPasswordResetConfirmView, self).get_success_url()
        print(url)
        return url


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'app_auth/password_reset_complete.html'


class UserLogoutView(LogoutView):
    next_page = 'home'
    # def get_next_page(self):
    #     pass
