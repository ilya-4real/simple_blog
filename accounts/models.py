from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse


class UserProfile(AbstractUser):
    GENDERS = (
        ('m', 'male'),
        ('f', 'female')
    )

    bio = models.TextField('bio', max_length=250, default='', unique=False)
    gender = models.CharField('gender', max_length=1, choices=GENDERS, default='', unique=False)

    def get_update_url(self):
        return reverse('user_update_url', kwargs={'user_id': self.id})
