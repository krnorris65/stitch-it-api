from django.db import models


class Fabric(models.Model):
    type = models.CharField(max_length=50)
    count = models.IntegerField()

    class Meta:
        ordering = ("type", "count")

    def __str__(self):
        return self.type
