from django.urls import path
from .views import *

urlpatterns = [
    path('posts/', PostsApiView.as_view(), name='posts_url'),
    path('tags/', TagsApiView.as_view(), name='tags.url'),
]
