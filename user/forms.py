from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

class SignupFrom(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email']
        labels = {'first_name': 'First Name', 'email': 'Email'}

class AdminChangeCustom(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = '__all__'

class UserChangeCustom(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email']#, 'date_joined', 'last_login']

