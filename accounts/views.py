from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .forms import RegisterUserForm
from .models import User


class RegisterUserView(CreateView):
    model = User
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:user-login')
    form_class = RegisterUserForm
    success_message = "User Create Successfully.Thank You"