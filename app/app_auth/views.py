from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView

from app_auth.forms import UserCreateForm


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
            user = form.save()
            print(user.org_name)
        return render(request, 'app_auth/sign_up.html', {'form': form})
