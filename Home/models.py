from django.db import models

from authentication.models import User


class Events(models.Model):

    created_by = models.ForeignKey(User, on_delete = models.PROTECT)
    cover = models.ImageField(upload_to='Events/')
    title = models.CharField(max_length = 255)
    description = models.TextField(max_length=700)

    def __str__(self) -> str:
        return self.title
    

class Places(models.Model):

    place_name = models.CharField(max_length = 255,null=True,blank=True)
    category = models.CharField(max_length = 255,null=True,blank=True)
    description = models.TextField(max_length = 1000,null=True,blank=True)
    location = models.CharField(max_length = 255,null=True,blank=True)
    fee = models.CharField(max_length = 255,null=True,blank=True)
    opening_hour = models.CharField(max_length = 255,null=True,blank=True)
    imeage = models.ImageField(upload_to='PlaceImeage/',null=True,blank=True)
    def __str__(self) -> str:
        return self.place_name