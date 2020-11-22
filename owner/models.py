from django.db import models
from django.contrib.auth.models import User as UserModel


class UserType(models.Model):
    user_type = models.CharField(max_length=12)

    def __str__(self):
        return self.user_type


class User(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
