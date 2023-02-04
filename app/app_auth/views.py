from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, UpdateView

from app_auth.forms import UserCreateForm, UserEditForm


class UserAuthView(LoginView):
    template_name = 'app_auth/login.html'

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
