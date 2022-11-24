from django import forms

class SigninForm(forms.Form):
    email = forms.CharField(label='email', max_length=100)
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', max_length=100)

class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', max_length=100)