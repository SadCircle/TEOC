from django.urls import path, re_path
from django.contrib.auth.decorators import login_required  
from .views import *

urlpatterns = [
    path('', login_required(parsers_listview.as_view()), name='parsers'),
    path('tg_channels/', login_required(tg_channels_listview.as_view()), name='tg_channels'),
    path('create/', parser_manager, name='parser_manager'),
]