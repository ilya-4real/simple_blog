from django.shortcuts import render
from rest_framework.generics import ListAPIView

from .serializers import PostSerializer
from blog.models import Post


class PostsApiView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
