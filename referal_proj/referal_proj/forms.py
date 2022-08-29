from doctest import DocTestRunner
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    referal_code = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'referal_code', 'password1', 'password2')

class LoginUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ('username', 'password')