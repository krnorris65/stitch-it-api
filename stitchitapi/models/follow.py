from django.db import models
from django.db.models import F
from .stitcher import Stitcher

class Follow(models.Model):

    follower = models.ForeignKey(Stitcher, on_delete=models.CASCADE, related_name="follows")
    stitcher = models.ForeignKey(Stitcher, on_delete=models.CASCADE, related_name="followers")
    pending = models.BooleanField()

    class Meta:
        ordering = (F('stitcher__user__last_name'), F('stitcher__user__first_name'))

    def __str__(self):
        return f'{self.follower.user.first_name} {self.follower.user.last_name} is following {self.stitcher.user.first_name} {self.stitcher.user.last_name}'