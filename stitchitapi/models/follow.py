from django.db import models
from .stitcher import Stitcher

class Follow(models.Model):

    follower = models.ForeignKey(Stitcher, on_delete=models.CASCADE)
    stitcher = models.ForeignKey(Stitcher, on_delete=models.CASCADE)
    pending = models.BooleanField()

    class Meta:
        ordering = ('stitcher.user.last_name', 'stitcher.user.first_name')

    def __str__(self):
        return f'{self.follower.user.first_name} {self.follower.user.last_name} is following {self.stitcher.user.first_name} {self.stitcher.user.last_name}'