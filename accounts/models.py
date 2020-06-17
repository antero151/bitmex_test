import uuid

from django.db import models

from utils.models import CUDate


class Account(CUDate):
    name = models.UUIDField(unique=True, default=uuid.uuid4(), blank=True)
    api_key = models.CharField(max_length=25)
    api_secret = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)
