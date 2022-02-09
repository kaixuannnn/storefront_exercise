from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    #we need to make the email field unique
    email = models.EmailField(unique=True)