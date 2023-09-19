from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from blog.models import Post, Tag


class TagSerializer(serializers.ModelSerializer):
    """
        built-in DRF model serializer
    """
    class Meta:
        model = Tag
        fields = ['title', 'slug']


class CustomTagSerializer(serializers.Serializer):
    """
    Custom tag serializer
    """
    title = serializers.CharField()
    slug = serializers.CharField()
    author = serializers.CharField()


class PostSerializer(ModelSerializer):
    """
    built-in DRF model serializer
    """
    class Meta:
        model = Post
        fields = ('title', 'slug', 'body', 'tags', 'pub_date', 'author',)


class CustomPostSerializer(serializers.Serializer):
    """
    Custom post serializer just to try
    """
    title = serializers.CharField()
    slug = serializers.CharField()
    body = serializers.CharField()
    tags = serializers.CharField()
    pub_date = serializers.DateTimeField()
    author = serializers.CharField()



