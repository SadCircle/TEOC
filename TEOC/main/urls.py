from django.urls import path,re_path
from .views import *


urlpatterns=[
    path('',index,name='main'),
    path('faq',faq,name='faq'),
    path('about',about,name='about'),
    
]