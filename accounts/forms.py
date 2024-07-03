from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Repeat Password")
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']

class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.UserNameInput(), label="Username")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    
    class Meta:
        model = User
        fields = ['username', 'password' ]
      