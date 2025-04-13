from django import forms
from django.forms.models import ModelForm
from django.core.exceptions import ValidationError
from .models import User

class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name","type"]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'type': forms.Select(attrs={
                'class': 'form-control',
            }),
        }