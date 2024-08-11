from django.contrib.auth.models import AbstractUser
from django.db import models

from utilities.models.base_model import BaseModel


class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True, db_index=True, null=True, blank=True)
    h = models.CharField()

    def __str__(self):
        return f"{self.username}-{self.created_at}"
