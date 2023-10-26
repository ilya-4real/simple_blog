from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from .tasks import resize_profile_image


class UserProfile(AbstractUser):
    GENDERS = (
        ('m', 'male'),
        ('f', 'female')
    )

    bio = models.TextField('bio', max_length=250, default='', blank=True)
    profile_image = models.ImageField(upload_to='images/', verbose_name='image', default='images/unknown_user.jpg')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print('asdfsdfasdf')
        resize_profile_image.delay(self.profile_image.path)

    def get_update_url(self):
        return reverse('user_update_url', kwargs={'user_id': self.id})
