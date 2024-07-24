# forms.py
from django import forms


class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True, label='First Name')
    last_name = forms.CharField(max_length=30, required=True, label='Last Name')
    email = forms.EmailField(required=True, label='Email')
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label='Password')


class SignInForm(forms.Form):
    email = forms.EmailField(max_length=30, required=True, label='Email')
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label='Password')


class NewPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label='New Password')
