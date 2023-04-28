from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class RoomForm(ModelForm):
    class Meta:
        model = Room
        # fields = '__all__'
        exclude = ['host', 'participants']


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
