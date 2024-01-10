from django.db import models

from authentication.models import User


class Events(models.Model):

    created_by = models.ForeignKey(User, on_delete = models.PROTECT)
    cover = models.ImageField(upload_to='Events/')
    title = models.CharField(max_length = 255)
    description = models.TextField(max_length=700)

    def __str__(self) -> str:
        return self.title