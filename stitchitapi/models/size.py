from django.db import models


class Size(models.Model):
    size = models.CharField(max_length=50)

    class Meta:
        ordering = ("size",)

    def __str__(self):
        return self.size
