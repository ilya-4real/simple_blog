from django import forms
from .models import *
from django.core.exceptions import ValidationError


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['title', 'slug']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'tag name'}),
            'slug': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'tag slug'})
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('You cannot create "create" tag!')
        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('This tag already exists!')
        return new_slug


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'tags']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Title of the post'}),
            'slug': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'slug'}),
            'body': forms.Textarea(attrs={'class': 'form-control mb-3', 'placeholder': 'Body'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select mb-3'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('You cannot create post with slug "create"')
        return new_slug
