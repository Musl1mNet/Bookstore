from django.contrib.auth.models import User
from django.db import models

class TelegramUser(models.Model):
    telegram_user_id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, default=None, blank=True)
    first_name = models.CharField(max_length=255, null=True, default=None, blank=True)
    last_name = models.CharField(max_length=255, null=True, default=None, blank=True)
    username = models.CharField(max_length=255, null=True, default=None, blank=True)
    language = models.CharField(max_length=5, default='uz')