from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, label="role")
    photo = forms.ImageField(required=False, label="photo")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'photo', 'password1', 'password2')
