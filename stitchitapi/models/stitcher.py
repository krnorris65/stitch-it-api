from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Stitcher(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_profile = models.BooleanField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = (F('user.last_name'), F('user.first_name'))