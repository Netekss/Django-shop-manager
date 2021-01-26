from django.db import models
from django.contrib.auth.models import User as UserModel


class User(models.Model):
    OWNER = 'owner'
    SELLER = 'seller'
    WAREHOUSEMAN = 'warehouseman'
    USER_TYPES = [
        (OWNER, OWNER),
        (SELLER, SELLER),
        (WAREHOUSEMAN, WAREHOUSEMAN)
    ]
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    user_type = models.CharField(choices=USER_TYPES, max_length=20)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
