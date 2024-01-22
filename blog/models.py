from django.db import models

from authentication.models import User


class BlogProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    total_review = models.FloatField(default=0)

    def __str__(self) -> str:
        return self.user.email


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length = 700)
    imeage = models.ImageField(upload_to="BlogImeage/", null=True, blank=True)


    def __str__(self) -> str:
        return self.title
