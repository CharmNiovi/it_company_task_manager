from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    profile_picture = models.ImageField(upload_to="profile_pictures", null=True, blank=True)
    email = models.EmailField(unique=True)
    position = models.ForeignKey(
        to=Position,
        on_delete=models.SET_NULL,
        null=True,
        related_name="workers"
    )
