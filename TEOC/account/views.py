from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
  
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect, HttpResponseRedirect

from .forms import *
# Create your views here.

def account_view(request):
    context = {
        'title': 'Акканут',
    }
    if request.user.is_authenticated:   
        return render(request, 'account/profile.html', context)
    else:
        return redirect('login')

class profile(UpdateView):
    model=User
    fields = ['first_name','last_name','username']
    template_name_suffix = '_update_form'



def signin_view(request):
    context = {
        'title': 'Регистрация',
    }

    if request.method == 'POST':    
        form = SigninForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            context = _check_on_exist(context,email,username)
            user = authenticate(username=username, password=raw_password)
            if context.get('email_used') or context.get('username_used'):
                context['form']=form
                return render(request, 'account/signin.html', context)
            User.objects.create_user(username, email, raw_password)
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            print(user)
            print('succes')
            return HttpResponseRedirect('../../')
    else:
        form = SigninForm()
        context['form']=form
    return render(request, 'account/signin.html', context)


def _check_on_exist(context,email,username):
    if User.objects.filter(email=email):
        context['email_used']=True
    if User.objects.filter(username=username):
        context['username_used']=True
    return context


def login_view(request):
    context = {
        'title': 'Вход',
    }
    if request.method == 'POST': 
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if user:
                login(request, user)
                return HttpResponseRedirect('../../')
            else:
                context['form']=form
                context['failed']=True
                return render(request, 'account/login.html', context)
    else:
        form = LoginForm()
        context['form']=form
        return render(request, 'account/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('main')

