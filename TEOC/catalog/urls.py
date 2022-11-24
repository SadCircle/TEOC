from django.urls import path, re_path
from django.contrib.auth.decorators import login_required 
from .views import *
# from django.urls.conf import include

urlpatterns = [
    path('', Documents.as_view(), name='catalog'),
    path('<int:pk>', Document_card.as_view(), name='document'),
    path('upload_files', login_required(upload_files), name='upload_files')
    # path('files_upload', FileFieldFormView.as_view(), name='model_form_upload')
]