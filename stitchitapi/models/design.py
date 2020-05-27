from django.db import models
from .fabric import Fabric
from .size import Size
from .stitcher import Stitcher


class Design(models.Model):

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255, null=True)
    completed_date = models.DateTimeField(null=True)
    photo = models.ImageField(upload_to="design/images/", null=True, blank=True)
    fabric = models.ForeignKey(Fabric, null=True, on_delete=models.SET_NULL)
    size = models.ForeignKey(Size, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(Stitcher, on_delete=models.CASCADE)

    class Meta:
        ordering = ('completed_date',)

    def __str__(self):
        return self.title
