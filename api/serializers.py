from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from blog.models import Post, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title', 'slug']


class CustomTagSerializer(serializers.Serializer):
    title = serializers.CharField()
    slug = serializers.CharField()
    author = serializers.CharField()

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'body', 'tags', 'pub_date', 'author',)


class CustomPostSerializer(serializers.Serializer):
    title = serializers.CharField()
    slug = serializers.CharField()
    body = serializers.CharField()
    tags = serializers.CharField()
    pub_date = serializers.DateTimeField()
    author = serializers.CharField()



