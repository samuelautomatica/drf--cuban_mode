from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.user