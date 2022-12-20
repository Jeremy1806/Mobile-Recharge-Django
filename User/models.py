from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    username = models.CharField(max_length=150, null=False, blank=False,unique=True)
    password = models.CharField(max_length=150, null=False, blank=False)
    wallet_balance = models.IntegerField(verbose_name="User Wallet Balance", default=100)
 
    USERNAME_FIELD = "username"
    PASSWORD_FIELD = "password"
