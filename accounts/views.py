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


class RegisterUserView(View):
    def get(self,request):
        form = RegisterUserForm()
        return render(request,"accounts/register.html",{'form':form})

    def post(self,request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.type== "Teacher":
                return redirect("exam:ask-question")
            else:
                return redirect("exam:quiz")
        return render(request,"accounts/register.html",{'form':form})
