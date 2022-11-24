from django.urls import path
from django.contrib.auth.decorators import login_required 
from .views import *


urlpatterns=[
    path('',login_required(account_view),name='account'),
    #path('signin/',signin_view,name='signin'),
    path('login/',login_view,name='login'),
    path('logout/',login_required(logout_view),name='logout')
]