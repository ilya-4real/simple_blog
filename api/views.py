from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from blog.models import Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related('author').prefetch_related('tags')
    serializer_class = PostSerializer

class PostsApiView(ListAPIView):
    queryset = Post.objects.all().select_related('author').prefetch_related('tags')
    serializer_class = CustomPostSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagsApiView(ListAPIView):
    queryset = (
        Tag.objects
        .select_related('author')
        .all()
        .values('title', 'slug', 'author__username')
    )
    serializer_class = TagSerializer


class PostsView(APIView):
    def get(self, request):
        queryset = Post.objects.all().values()
        return Response({'posts': list(queryset)})

    def post(self, request):
        if request.user.is_authenticated:
            post = Post.objects.create(
                title=request.data['title'],
                slug=request.data['slug'],
                body=request.data['body'],
                tags=request.data['tags'],
                author=request.user
            )
        else:
            post = Post.objects.get(pk=13)
        return Response({'post': model_to_dict(post)})
