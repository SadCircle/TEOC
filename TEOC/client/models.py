from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.


class Parser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    api_id = models.CharField(max_length=255)
    api_hash = models.CharField(max_length=255)
    session = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    phone_code_hash = models.CharField(max_length=255)
    auth = models.BooleanField(default=False)
    in_progress = models.BooleanField(default=False)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    time_beat_duration = models.DurationField(default=datetime.timedelta(days =1))
    auto = models.BooleanField(default=False)

class Tg_Channels(models.Model):
    url = models.CharField(max_length=255)
