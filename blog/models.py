from django.db import models
from django.shortcuts import reverse
from accounts.models import UserProfile


from blog.modules.services import post_slugifier, tag_slugifier


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    body = models.TextField(blank=True, db_index=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(UserProfile, on_delete=models.PROTECT, related_name='posts')

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = post_slugifier(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-pub_date']


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    author = models.ForeignKey(UserProfile, on_delete=models.PROTECT, related_name='tag')

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = tag_slugifier(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['title']


class Comment(models.Model):
    body = models.TextField(max_length=250)
    author = models.ForeignKey(UserProfile, on_delete=models.PROTECT, related_name='comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

