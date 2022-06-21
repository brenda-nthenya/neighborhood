from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime as dt
# Create your models here.

class Neighborhood(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    occupants_count = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)
    Admin = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

