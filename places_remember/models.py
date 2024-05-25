from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass


class Coordinates(models.Model):
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.lat} - {self.lng}'


class Memory(models.Model):
    author = models.ForeignKey(
        CustomUser,
        null=True,
        related_name='memories',
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=200)
    comment = models.TextField(max_length=1000)
    coordinates = models.ForeignKey(
        Coordinates,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.title}'
