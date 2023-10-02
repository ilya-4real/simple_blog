from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    GENDERS = (
        ('m', 'male'),
        ('f', 'female')
    )

    bio = models.TextField('bio', max_length=250, default='')
    gender = models.CharField('gender', max_length=1, choices=GENDERS, default='')
