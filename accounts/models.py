from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse


class UserProfile(AbstractUser):
    GENDERS = (
        ('m', 'male'),
        ('f', 'female')
    )

    bio = models.TextField('bio', max_length=250, default='', blank=True)
    profile_image = models.ImageField(upload_to='images/', verbose_name='images', default='images/unknown_user.jpg')

    def get_update_url(self):
        return reverse('user_update_url', kwargs={'user_id': self.id})
