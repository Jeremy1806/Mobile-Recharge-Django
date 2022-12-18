from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    email = models.EmailField(
        max_length=150, null=False, blank=False, unique=True)
    password = models.CharField(max_length=150, null=False, blank=False)

    REQUIRED_FIELDS = ["username"]

    USERNAME_FIELD = "email"
    PASSWORD_FIELD = "password"
